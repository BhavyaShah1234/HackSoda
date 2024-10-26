from deepface import DeepFace

class Verifier:
    def __init__(self, model_name='Facenet512'):
        self.model_name = model_name

    def verify(self, img_path1, img_path2, threshold=0.7):
        result = DeepFace.verify(img_path1, img_path2, self.model_name, anti_spoofing=True, threshold=threshold)
        return result

if __name__ == '__main__':
    img_path1 = ''
    img_path2 = ''
    model = Verifier()
    result = model.verify(img_path1, img_path2)
    print(result)
