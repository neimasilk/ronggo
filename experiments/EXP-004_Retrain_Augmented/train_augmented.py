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
from transformers.trainer_utils import get_last_checkpoint

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DATA_PATH = os.path.join(SCRIPT_DIR, "../EXP-003_DeepSeek_Augmentation/augmented_train_v1.csv")
VAL_DATA_PATH = os.path.join(SCRIPT_DIR, "../../dataset/val.csv")
TEST_DATA_PATH = os.path.join(SCRIPT_DIR, "../../dataset/test.csv")

MODEL_CHECKPOINT = "facebook/nllb-200-distilled-600M"
SRC_LANG = "ind_Latn"
TGT_LANG = "eng_Latn"
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_model")

# Hyperparameters
MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 20
WEIGHT_DECAY = 0.01

def main():
    print(f"--- EXP-004: Retraining with Augmented Data ---")
    print(f"Train Data: {TRAIN_DATA_PATH}")
    
    if not os.path.exists(TRAIN_DATA_PATH):
        raise FileNotFoundError(f"File dataset {TRAIN_DATA_PATH} tidak ditemukan. Jalankan EXP-003 dulu!")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1. Load Dataset
    data_files = {
        "train": TRAIN_DATA_PATH,
        "validation": VAL_DATA_PATH,
        "test": TEST_DATA_PATH,
    }
    dataset = load_dataset("csv", data_files=data_files)
    
    # 2. Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_CHECKPOINT)
    
    tokenizer.src_lang = SRC_LANG
    tokenizer.tgt_lang = TGT_LANG
    model.config.forced_bos_token_id = tokenizer.convert_tokens_to_ids(TGT_LANG)

    # 3. Preprocessing
    def preprocess_function(examples):
        inputs = [str(ex) for ex in examples["indonesian"]] 
        targets = [str(ex) for ex in examples["papua_kokas"]]
        
        model_inputs = tokenizer(
            inputs, 
            text_target=targets,
            max_length=MAX_INPUT_LENGTH, 
            truncation=True, 
            padding=True
        )
        return model_inputs

    cols_to_remove = dataset["train"].column_names
    tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=cols_to_remove)

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
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        result = {"bleu": result["score"]}
        return {k: round(v, 4) for k, v in result.items()}

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
        fp16=torch.cuda.is_available(),
        logging_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="bleu",
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )

    # 6. Train with Resume Logic
    print("Starting training...")
    last_checkpoint = None
    if os.path.isdir(OUTPUT_DIR):
        last_checkpoint = get_last_checkpoint(OUTPUT_DIR)
        if last_checkpoint:
            print(f"Resuming training from checkpoint: {last_checkpoint}")
    
    trainer.train(resume_from_checkpoint=last_checkpoint)

    # 7. Evaluate on Test Set
    print("Evaluating on Test Set...")
    test_results = trainer.predict(tokenized_datasets["test"])
    print("Test Results:", test_results.metrics)

    trainer.save_model(os.path.join(OUTPUT_DIR, "final_model"))
    print("Model saved.")

if __name__ == "__main__":
    main()