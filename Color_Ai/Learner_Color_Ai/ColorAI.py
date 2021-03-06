import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import datetime
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.image as mpimg
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from PIL import Image

class ColorAI():
    def __init__(self, n_neighbors = 15):
        self.trained_data = pd.read_csv("learned_color_data.csv")
        self.number_of_neighbors = n_neighbors
    
    
    def showMethods(self):
        print("showDataMemory, accuracyTest, getColor, showDataFrame, teach, getColorFromImage")
    

    def showDataMemory(self):
        color_name_guide = self.trained_data["Color name"]
        result_color_name = color_name_guide.drop_duplicates()

        color_id = self.trained_data["Id"]
        result_color_id = color_id.drop_duplicates()
        user_guide = pd.DataFrame({"Color family" : result_color_name, "ID" : result_color_id})

        print(user_guide)
    
    
    def accuracyTest(self):
        test_data = self.trained_data

        X = test_data.iloc[:, :-2].values
        y = test_data["Id"]


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        knn = KNeighborsClassifier(n_neighbors = self.number_of_neighbors)
        knn.fit(X_train, y_train)

        y_pred = knn.predict(X_test)
        
        print(y_pred)
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
        
    
    def getColor(self, color_inp, data_ref, ret_val = "False", show_predicted = True):
        self.data = data_ref

        R = self.data["R"]
        G = self.data["G"]
        B = self.data["B"]

        X = self.data.iloc[:, :-2].values
        y = self.data["Id"]


        model = KNeighborsClassifier(n_neighbors = self.number_of_neighbors)
        model.fit(X, y)


        u_input = color_inp


        prediction = model.predict([u_input])

        self.prediction_index = np.where(self.data == prediction[0])[0][0]
        
        if show_predicted == True:
            print("prediction:", self.data["Color name"][self.prediction_index])
            
        elif show_predicted == False:
            pass
        
        else:
            print("no such parameter")
        
        
        if ret_val == True:
            return prediction

    
    def showDataFrame(self):
        pd.set_option("display.max_rows", 10000)
        print(self.trained_data)
    
    
    
    def teach(self, save_count = 1):
        teach_status = "T"
        n_test = 0
        n_correct = 0
        n_wrong = 0
        
        while teach_status == "T":
            print("-" * 10 + str(n_test) +"-" * 10)
            
            n_test += 1
            
            uinp = input("color:")
            uinp_enc = re.split(",", uinp)
            print("inp", uinp_enc)
            RGB = []
            
            for num in uinp_enc:
                print(num)
                RGB.append(int(num))
            
            print("rgb", type(RGB[1]))

            self.getColor(RGB, self.trained_data)

            answer_status = input("answer status C/W:")

            if answer_status == "C":
                n_correct += 1
                
                R = RGB[0]
                G = RGB[1]
                B = RGB[2]
                
                print(R, G, B)
                save_count = save_count
                while save_count > 0:
                    shade_fam = self.data["Color name"][self.prediction_index]
                    data_id = self.data["Id"][self.prediction_index]
                    new_data = pd.DataFrame({"R":R, "G":G, "B":B, "Color name":shade_fam, "Id":data_id}, index = [0])

                    self.trained_data = pd.concat([new_data, self.trained_data]).reset_index(drop = True)
                    self.trained_data.to_csv("learned_color_data.csv", index=False)
                    
                    save_count -= 1
                    if save_count == 0: break
                    
                    

            elif answer_status == "W":
                R = RGB[0]
                G = RGB[1]
                B = RGB[2]
                
                n_wrong += 1

                add_learnings = input("Add New Lesson? Y/N :")
                
                if add_learnings == "Y":
                    
                    
                    self.showDataMemory()
                    
                    shade_fam = input("shader family:")
                    data_id = int(input("new data id:"))
                    
                    save_count = save_count
                    
                    while save_count > 0:
                        new_data = pd.DataFrame({"R":R, "G":G, "B":B, "Color name":shade_fam, "Id":data_id}, index = [0])

                        self.trained_data = pd.concat([new_data, self.trained_data]).reset_index(drop = True)
                        self.trained_data.to_csv("learned_color_data.csv", index=False)
                        
                        save_count -= 1
                        if save_count == 0: break
            
            else:
                print("input error")
                break
                             
            
            if teach_status == "F":
                print("-" * 10 + "teaching ended" + "-" * 10)
                print("number of tests : ", n_test)
                print("correct answer : ", n_correct)
                print("wrong answer : ", n_wrong)
                break
            
            teach_status = input("teaching status T/F:")
            
                
                
                
    def getColorFromImage(self, show_plot = False, show_info = False, read_img = "strips"):
        uinp = input("image:")
  
        if read_img == "strips":
            print("analizyng image")
            
            try:
                image_inp = mpimg.imread(uinp)
            except Exception as error:
                print(error)
  

            image_size = np.array(image_inp)
            image_total_pixel = int((image_inp.shape[2] * image_inp.shape[1] * image_inp.shape[0]))

            dim1 = int(image_total_pixel / 3)

            image_data = image_size.reshape(dim1, 3)

            seq_shape = int((image_inp[0:50].shape[2] * image_inp[0:50].shape[1] * image_inp[0:50].shape[0]) / 3)

            sequence_1 = np.array(image_inp[0:50]).reshape(seq_shape, 3)
            sequence_2 = np.array(image_inp[ int(image_inp.shape[0] / 2): int((image_inp.shape[0] / 2) + 50)]).reshape(seq_shape, 3)
            sequence_3 = np.array(image_inp[ int(image_inp.shape[0] - 50 ): int(image_inp.shape[0])]).reshape(seq_shape, 3)


            print("---" * 15 + "---" * 15 )

            if show_plot == True:
                fig, axs = plt.subplots(3)


                axs[0].imshow(image_inp[0:50])
                axs[1].imshow(image_inp[ int(image_inp.shape[0] / 2): int((image_inp.shape[0] / 2) + 50)])
                axs[2].imshow(image_inp[ int(image_inp.shape[0] - 50 ): int(image_inp.shape[0])])



            readings = np.array([sequence_1, sequence_2, sequence_3])
            tota_pixels = readings.shape[2]* readings.shape[1] * readings.shape[0]

            enc_reading = readings.reshape(int(tota_pixels / 3), 3)


            data = pd.read_csv("learned_color_data.csv")

            Red_pixel = data["R"]
            Green_pixel = data["G"]
            Blue_pixel = data["B"]

            feat = np.array([Red_pixel, Green_pixel, Blue_pixel])


            X = data.iloc[:, :-2].values
            y = data["Id"]

            
            model = RandomForestClassifier(max_depth=100, random_state=0)
            model.fit(X, y)

            prediction = model.predict(enc_reading)


            result_color_name = pd.DataFrame({"answers" : prediction}).drop_duplicates()

            answers = np.array(result_color_name["answers"])


            if show_info == True:
                print("INFORMATION:" + "\n")
                print("colors found", answers)
                self.showDataMemory()


            turn = 0
            n_total = 0
            ans_arr = []

            for index in answers:
                for pixel in prediction:
                    if pixel == answers[turn]:
                        n_total += 1

                turn += 1
                ans_arr.append(n_total)
                n_total -= n_total

                if turn >= answers.shape[0]:
                    break

            superior = np.max(ans_arr)
            answer_index = ans_arr.index(superior)

            final_answer_index = answers[answer_index]
            final_answer = np.where(data["Id"] == final_answer_index)[0][0]

            print("\n" + "Prominent Color:", data["Color name"].iloc[final_answer])
        
        
        if read_img == "full":
            print("analyzing image. It will take time depending on the size of the image and tour proccesssing power")
            
            res_img = Image.open(uinp)
            
            img_height = res_img.size[1]
            img_width = res_img.size[0]

            res_img = res_img.resize((int(img_width / 2), int(img_height / 2)),Image.ANTIALIAS)
            res_img.save("images/res_image.jpg",optimize=True,quality=100)
            
            res_img = mpimg.imread("images/res_image.jpg")
        
            img_array = np.array(res_img)
            
            print(img_array.shape)
            
            dimension = img_array.shape[0] * img_array.shape[1]
            img_array = img_array.reshape(dimension, 3)
            
            print(img_array.shape)
            
            color_found = []
            
            data = pd.read_csv("learned_color_data.csv")
            
            count = 0
            for color in img_array:               
                color_found.append(self.getColor(color, data, ret_val = True, show_predicted = False)[0])
                print(color_found)
                count += 1
                
                if count >= 20:
                    break
                
            
            result_color_name = pd.DataFrame({"answers" : color_found}).drop_duplicates()
            answers = np.array(result_color_name["answers"])
            
            self.showDataMemory()
            print("found colors:", answers)