from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=True, src_lang="ron_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=True)

article = "Şeful ONU spune că nu există o soluţie militară în Siria"
inputs = tokenizer(article, return_tensors="pt")

translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["deu_Latn"], max_length=30)

print(tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0])
