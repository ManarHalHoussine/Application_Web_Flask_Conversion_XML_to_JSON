from flask import Flask, render_template, request
import json
import xmltodict

app = Flask(__name__)


def is_xml(data):
    try:
        xmltodict.parse(data)
        return True
    except Exception as e:
        return False


def is_json(data):
    try:
        json.loads(data)
        return True
    except Exception as e:
        return False


def convert_json_to_xml(json_string):
    json_dict = json.loads(json_string)
    xml_string = xmltodict.unparse(json_dict, pretty=True)
    return xml_string


def convert_xml_to_json(xml_string):
    xml_dict = xmltodict.parse(xml_string)
    json_string = json.dumps(xml_dict, indent=4)
    return json_string


@app.route('/', methods=['GET', 'POST'])
def index():
    input_content = ""
    output_content = ""

    if request.method == 'POST':
        if 'convert_button' in request.form:
            input_content = request.form['zone_input']

            if is_json(input_content):
                output_content = convert_json_to_xml(input_content)
            elif is_xml(input_content):
                output_content = convert_xml_to_json(input_content)
            else:
                output_content = "Entrer un code XML ou JSON"
        elif 'upload_button' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file:
                file_content = uploaded_file.read().decode('utf-8')
                if is_json(file_content):
                    output_content = convert_json_to_xml(file_content)
                elif is_xml(file_content):
                    output_content = convert_xml_to_json(file_content)
                # Affiche le contenu du fichier uploadé dans la zone de texte d'entrée
                input_content = file_content

    return render_template('index.html', output_content=output_content, input_content=input_content)


if __name__ == '__main__':
    app.run(debug=True)
