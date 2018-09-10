import sys
from lxml import etree
import math
import subprocess
import csv





for a in ['both','male', 'female']:
    for b in ['_very_','_high_', '_medium_', '_low_']:

        graph_title = b+a

        for i in range(0,3):
            subprocess.call(['inkscape','--without-gui', '--export-plain-svg=./temp/bar'+b+a+'_'+str(i)+'.svg', './temp/bar'+b+a+'_'+str(i)+'.eps'], shell=True)
            print('bar'+b+a+'_'+str(i) + " convert")
            subprocess.call(['inkscape','--without-gui', '--export-plain-svg=./temp/pie'+b+a+'_'+str(i)+'.svg', './temp/pie'+b+a+'_'+str(i)+'.eps'], shell=True)
            print('pie'+b+a+'_'+str(i) + " convert")


        lab_cancer = ["temp", "temp", "temp", "temp", "temp","temp", "temp", "temp", "temp", "temp","temp", "temp", "temp", "temp", "temp"]
        lab_pos = [0, 0, 0, 0, 0,0, 0, 0, 0, 0,0, 0, 0, 0, 0]
        pop_size= [0, 0, 0, 0, 0, 0]


        label_file = open('./temp/cancer_label'+b+a+'.csv', newline='')
        cancer_list = list(csv.reader(label_file, delimiter=',', quotechar='"'))



        i = 0



        for x in cancer_list:
            if i > 0:
                lab_cancer[i-1] = x[0]
                lab_pos[i-1] = x[1]
            i = i +1



        number_file = open('./temp/cancer_number'+b+a+'.csv', newline='')
        cancer_number = list(csv.reader(number_file, delimiter=',', quotechar='|'))

        i = 0


        for x in cancer_number:
            if i > 0:
                pop_size[i-1] = int(x[0])
            i = i +1




        pie_size= [0,0,0]
        pie_file = ["./temp/pie"+b+a+"_0.svg", "./temp/pie"+b+a+"_1.svg", "./temp/pie"+b+a+"_2.svg"]
        bar_file = ["./temp/bar"+b+a+"_0.svg", "./temp/bar"+b+a+"_1.svg", "./temp/bar"+b+a+"_2.svg"]
        bar_scale = ["-2.5593047", "356.80114", "698.53954"]

        pie_size[0] = math.sqrt( pop_size[0]/pop_size[4]) * 200
        pie_size[1] = math.sqrt( pop_size[2]/pop_size[4]) * 200
        pie_size[2] = 200


        percent_size= [0,0,0,0,0,0]
        percent_size[0] = round((pop_size[1]/pop_size[0])*100, 1)
        percent_size[1] = round(((pop_size[0]- pop_size[1])/pop_size[0])*100, 1)
        percent_size[2] = round((pop_size[3]/pop_size[2])*100, 1)
        percent_size[3] = round(((pop_size[2]- pop_size[3])/pop_size[2])*100, 1)
        percent_size[4] = round((pop_size[5]/pop_size[4])*100, 1)
        percent_size[5] = round(((pop_size[4]- pop_size[5])/pop_size[4])*100, 1)

        base = etree.parse(open('./pie_bar_base.svg'))
        root = base.getroot()

        for i in range(0,3):


            base_pie = etree.parse(open(pie_file[i]))
            root_pie = base_pie.getroot()
            pie = root_pie[2]


            pie[0].remove(pie[0][5])
            pie[0].remove(pie[0][0])

            temp = pie[0]

            scale = (pie_size[i]/268.533)*0.1

            temp.set("transform", "matrix(" + str(scale) + ",0,0,"+ str(scale*-1) + "," + str(i*400) + ",0)")

            root.append(temp)

            base_bar = etree.parse(open(bar_file[i]))
            root_bar = base_bar.getroot()


            bar = root_bar[2]


            bar[0].remove(bar[0][0])

            temp = bar[0]


            temp.set("style", "stroke-width:3.12442231")
            temp.set("transform", "matrix(0.0226505,0,0,-0.04522544," + bar_scale[i]+",433.45037)")
            root.append(temp)






        for child in root[3]:
            if len(child.getchildren()) == 1:
                for i in range(0,6):
                    if child[0].text == str(i+1)+"%":
                        child[0].text = str(percent_size[i])+"%"
                    if child[0].text == str(i+1):
                        child[0].text = lab_cancer[i]
                        child.set('y', lab_pos[i])
                    if child[0].text == str(i+1+5):
                        child[0].text = lab_cancer[i+5]
                        child.set('y', lab_pos[i+5])
                    if child[0].text == str(i+1+10):
                        child[0].text = lab_cancer[i+10]
                        child.set('y', lab_pos[i+10])


                if child[0].text == "Title":
                    child[0].text = graph_title
            if len(child.getchildren()) == 2:
                for i in range(0,3):
                    if child[0].text == str((i+1)*1000):
                        if pop_size[i*2] > 1000000:
                            child[0].text = str((round(pop_size[i*2]/1000000,1))) + " million"
                        else:
                            child[0].text = str(int(round(pop_size[i*2]/1000,0))*1000)
            if len(child.getchildren()) == 10:
                print(child)




        base.write('./temp'+b+a+'.svg', pretty_print=False)





