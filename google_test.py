from googletrans import Translator

translator = Translator()

translated_text = translator.translate("Bonjour")

print('translated text: ', translated_text.text)