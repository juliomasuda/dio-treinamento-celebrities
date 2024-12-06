from pathlib import Path
import boto3
from mypy_boto3_rekognition.type_defs import CompareFacesMatchTypeDef, CelebrityTypeDef
from PIL import Image, ImageDraw, ImageFont


#session = boto3.Session(profile_name='profile-name')
client = boto3.client('rekognition')

def get_path(file_name: str) -> str:
    return str(Path(__file__).parent / "images" / file_name)


def recognize_in_photo(photo):
    
    with open(photo, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    print('Detected faces for ' + photo)
    for celebrity in response['CelebrityFaces']:
        print('Name: ' + celebrity['Name'])
    #    print('Id: ' + celebrity['Id'])
    #    print('KnownGender: ' + celebrity['KnownGender']['Type'])
    #    print('Smile: ' + str(celebrity['Face']['Smile']['Value']))
    #    print('Position:')
    #    print('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
    #    print('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
        confidence = celebrity["MatchConfidence"]
        print(f"Confidence: {confidence:.1f}%")
    #    print('Info')
    #    for url in celebrity['Urls']:
    #        print('   ' + url)
        print()
    #return len(response['CelebrityFaces'])

    return response

def draw_boxes(
    image_path: str, output_path: str, face_details: list[CompareFacesMatchTypeDef]
) -> None:
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    width, height = image.size

    for face in face_details:
        
        confidence = face["MatchConfidence"]
        if confidence > 99.9:
            box = face["Face"]["BoundingBox"]
            left = int(box["Left"] * width)
            top = int(box["Top"] * height)
            right = int((box["Left"] + box["Width"]) * width)
            bottom = int((box["Top"] + box["Height"]) * height)

            draw.rectangle([left, top, right, bottom], outline="red", width=3)

            
            name = face["Name"]

            fontSize = 30
            font = ImageFont.truetype('arial.ttf', fontSize)
            #draw.text( 
            #    (left, top - 30), f"{confidence:.1f}%", fill = "red", font = font
            #)
            draw.text( 
                (left, top - 30), f"{name}", fill = "red", font = font
            )
            image.save(output_path)
            print(f"Imagem salva com resultados em: {output_path}")


def recognize_celebrities(foto_path: str, result_path: str):

    response = recognize_in_photo(foto_path)

    if response['CelebrityFaces']:
        draw_boxes(foto_path, result_path, response["CelebrityFaces"])
        return True
    
    return False

if __name__ == "__main__":
    real_madrid_path = get_path("real_madrid.jpg")
    barcelona_path = get_path("barcelona.jpg")
    neymar_path = get_path("neymar1.jpg")

    real_madrid_output = get_path("real_madrid_result.jpg")
    barcelona_output = get_path("barcelona_result.jpg")
    neymar_output = get_path("neymar_result.jpg")

    if not recognize_celebrities(real_madrid_path, real_madrid_output):
        print(f"Nenhuma celebridade encontrada em {real_madrid_path}")

    if not recognize_celebrities(barcelona_path, barcelona_output):
        print(f"Nenhuma celebridade encontrada em {barcelona_path}")

    if not recognize_celebrities(neymar_path, neymar_output):
        print(f"Nenhuma celebridade encontrada em {neymar_path}")



