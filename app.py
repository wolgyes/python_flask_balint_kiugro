from flask import Flask, render_template, request
from loguru import logger
from deep_translator import GoogleTranslator
app = Flask(__name__)

resp = {
    'langs': {"auto": "Automatikus", "hu": "Hungarian", "en": "English", "de": "German", "fr": "French", "es": "Spanish",
         "it": "Italian",
         "pt": "Portuguese", "nl": "Dutch", "pl": "Polish", "ru": "Russian", "ja": "Japanese", "zh": "Chinese"},
    'word': '',
    'source_lang': {'key': 'auto', 'value': 'Automatikus'},
    'target_lang': {'key': 'hu', 'value': 'Hungarian'}
}



def translate_text(text, source="auto", target='hu'):
    return GoogleTranslator(source=source, target=target).translate(text)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        s_l = request.form.get("source_lang")
        logger.info(s_l)
        t_l = request.form.get("target_lang")
        resp['source_lang']['key'] = s_l
        resp['source_lang']['value'] = resp['langs'][s_l]
        resp['target_lang']['key'] = t_l
        resp['target_lang']['value'] = resp['langs'][t_l]

        word = request.form.get("word")

        if word:
            resp['word'] = translate_text(word, source=s_l, target=t_l)
            return render_template('home.html', data=resp)
        else:
            logger.warning("No word provided")
            return render_template('home.html', data=resp)

    return render_template('home.html', data=resp)


if __name__ == '__main__':
    app.debug = True
    app.run()
