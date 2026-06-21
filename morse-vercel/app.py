from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',

    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..',  '9': '----.',

    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.',  '(': '-.--.',  ')': '-.--.-',
    '&': '.-...',  ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.',  '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-','@': '.--.-.',
}

REVERSE_MORSE = {v: k for k, v in MORSE_CODE.items()}


def text_to_morse(text):
    text = text.upper()
    words = text.split(' ')
    morse_words = []
    unknown = []

    for word in words:
        morse_chars = []
        for char in word:
            if char in MORSE_CODE:
                morse_chars.append(MORSE_CODE[char])
            else:
                morse_chars.append('?')
                if char not in unknown:
                    unknown.append(char)
        morse_words.append(' '.join(morse_chars))

    return ' / '.join(morse_words), unknown


def morse_to_text(morse):
    words = morse.strip().split(' / ')
    result = []
    unknown = []

    for word in words:
        chars = word.strip().split(' ')
        decoded = []
        for code in chars:
            code = code.strip()
            if not code:
                continue
            if code in REVERSE_MORSE:
                decoded.append(REVERSE_MORSE[code])
            else:
                decoded.append('?')
                if code not in unknown:
                    unknown.append(code)
        result.append(''.join(decoded))

    return ' '.join(result), unknown




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    data      = request.get_json()
    text      = data.get('text', '')
    direction = data.get('direction', 'to_morse')

    if not text.strip():
        return jsonify({'result': '', 'unknown': []})

    if direction == 'to_morse':
        result, unknown = text_to_morse(text)
    else:
        result, unknown = morse_to_text(text)

    return jsonify({'result': result, 'unknown': unknown})
