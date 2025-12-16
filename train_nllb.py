import os
import torch
import numpy as np
import evaluate
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)

# --- Configuration ---
MODEL_CHECKPOINT = "facebook/nllb-200-distilled-600M"
SRC_LANG = "ind_Latn"  # Indonesian
TGT_LANG = "eng_Latn"  # Placeholder for Sekar (Papua Kokas)
MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 5
WEIGHT_DECAY = 0.01
OUTPUT_DIR = "./nllb-sekar-finetuned"

def main():
    print(f"Using device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

    # 1. Load Dataset
    data_files = {
        "train": "dataset/train.csv",
        "validation": "dataset/val.csv",
        "test": "dataset/test.csv",
    }
    dataset = load_dataset("csv", data_files=data_files)
    
    print("Dataset loaded:")
    print(dataset)

    # 2. Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_CHECKPOINT)
    
    # Set Language Codes
    tokenizer.src_lang = SRC_LANG
    tokenizer.tgt_lang = TGT_LANG
    # Ensure the model generates the correct target language
    model.config.forced_bos_token_id = tokenizer.convert_tokens_to_ids(TGT_LANG)

    # 3. Preprocessing
    def preprocess_function(examples):
        inputs = [ex for ex in examples["indonesian"]]
        targets = [ex for ex in examples["papua_kokas"]]
        
        model_inputs = tokenizer(
            inputs, 
            text_target=targets,
            max_length=MAX_INPUT_LENGTH, 
            truncation=True, 
            padding=True
        )
        return model_inputs

    tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

    # 4. Metrics
    metric = evaluate.load("sacrebleu")

    def postprocess_text(preds, labels):
        preds = [pred.strip() for pred in preds]
        labels = [[label.strip()] for label in labels]
        return preds, labels

    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        if isinstance(preds, tuple):
            preds = preds[0]
        
        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

        # Replace -100 in the labels as we can't decode them.
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        result = {"bleu": result["score"]}

        prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result

    # 5. Trainer Setup
    args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        weight_decay=WEIGHT_DECAY,
        save_total_limit=2,
        num_train_epochs=NUM_EPOCHS,
        predict_with_generate=True,
        fp16=True, # Enable mixed precision for T4
        logging_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="bleu",
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # 6. Train
    print("Starting training...")
    trainer.train()

    # 7. Evaluate on Test Set
    print("Evaluating on Test Set...")
    test_results = trainer.predict(tokenized_datasets["test"])
    print("Test Results:", test_results.metrics)

    trainer.save_model(os.path.join(OUTPUT_DIR, "final_model"))
    print("Model saved.")

if __name__ == "__main__":
    main()
