from pylatex import *
from pylatex.utils import *
from pylatex.base_classes import Float

# import sys
# sys.path.append(r"")

import importlib
QnA_module = importlib.import_module("Neurologie cellulaire")


#Replaces all % by \% so that LaTeX doesn't comment out text
for i in range(len(QnA_module.question_list)):
    for j in range(len(QnA_module.question_list[i])):
        if isinstance(QnA_module.question_list[i][j], str) and '%' in QnA_module.question_list[i][j]:
            QnA_module.question_list[i][j] = QnA_module.question_list[i][j].replace('%', '\\%')

        elif isinstance(QnA_module.question_list[i][j], list) and len(QnA_module.question_list[i][j]) > 1:
            for k in range(len(QnA_module.question_list[i][j])):
                if isinstance(QnA_module.question_list[i][j][k], str):
                    QnA_module.question_list[i][j][k] = QnA_module.question_list[i][j][k].replace('%', '\\%')


if __name__ == '__main__':  
    geometry_options = {"tmargin": "1cm"} #tmargin=y, lmargin=x | There are other ways to do this | 1cm better without date, else 2cm
    doc = Document(geometry_options=geometry_options)
    
    #Increases dpi, grabbed it from stackoverflow
    # doc.preamble.append(NoEscape(r'\pdfpxdimen=1in'))
    # doc.preamble.append(NoEscape(r'\divide\pdfpxdimen by 96'))

    #In LaTeX, floats are used to contain things that must be placed inside a single page, i.e., they cannot be broken over multiple pages.
    doc.preamble.append(Package('Float'))


    #Making the title
    doc.preamble.append(Command('title', 'Q&A : ' + QnA_module.title))
    # doc.preamble.append(Command('author', ''))
    doc.preamble.append(Command('date', '')) #If a date isn't defined, it will put the current one
    doc.append(NoEscape(r'\maketitle'))



    #Document
    for i in range(len(QnA_module.question_list)):
        # with doc.create(Figure(position='h!t')) as doc:
        with doc.create(Section(f"Question {i+1}", False)):
            #Question
            doc.append(NoEscape(f'\\Large \\hspace{{1cm}} {QnA_module.question_list[i][0]} \\\\')) #size carries over

            #Question worth
            if QnA_module.question_list[i][3] > 1:
                #LaTeX normally removes horizontal space that comes at the beginning or end of a line. To preserve this space, use the optional * form [of \hspace].
                doc.append(NoEscape(f'\\footnosize \\hspace*{{5.3cm}} (This question is worth {QnA_module.question_list[i][3]} points.) \\normalsize \\\\'))
            else: doc.append(NoEscape(f'\\footnotesize \\hspace*{{5.3cm}} (This question is worth {QnA_module.question_list[i][3]} point.) \\normalsize \\\\'))

            #Question images
            if QnA_module.question_list[i][4]:
                with doc.create(Center()):
                    
                    #If multiple
                    if isinstance(QnA_module.question_list[i][4], list) or isinstance(QnA_module.question_list[i][4], tuple):
                        with doc.create(Figure(position='H')) as img:
                            for image in QnA_module.question_list[i][4]:
                                img.add_image(image)
                                img.append('\n')

                    else: #If only one
                        with doc.create(Figure(position='H')) as img:
                            img.add_image(QnA_module.question_list[i][4])

            with doc.create(Figure(position='H')):
                #Choices
                with doc.create(Subsection('Choices :', False)):
                    with doc.create(Description()) as item:

                        for n in range(len(QnA_module.question_list[i][1])): #{{}} escapes f-strings and not \{\}
                            item.add_item('', NoEscape(f"\\hspace{{1cm}} – \\hspace{{0.25cm}} {QnA_module.question_list[i][1][n]}"))

            with doc.create(Figure(position='H')):
                #if order
                order_check = ''
                if QnA_module.question_list[i][7]:
                    if isinstance(QnA_module.question_list[i][7], str) and QnA_module.question_list[i][7].lower() == 'numbers':
                        with doc.create(Subsection('Answers in numbered order :', False)):
                            with doc.create(Description()) as item:

                                for n in range(len(QnA_module.question_list[i][2])):
                                    item.add_item('', NoEscape(f"\\hspace{{1cm}} {n+1}) \\hspace{{0.25cm}} {QnA_module.question_list[i][2][n]}"))


                    elif isinstance(QnA_module.question_list[i][7], str) and QnA_module.question_list[i][7].lower() == 'letters':
                        with doc.create(Subsection('Answers in lettered order :', False)):
                            with doc.create(Description()) as item:

                                for answer in range(len(QnA_module.question_list[i][2])):
                                    k = QnA_module.question_list[i][1].index(answer)
                                    item.add_item('', NoEscape(f"\\hspace{{1cm}} {chr(k+65)}) \\hspace{{0.25cm}} {answer}"))

                    order_check = 'in order'

                else:
                    with doc.create(Subsection(f'Answers {order_check} :', False)):
                        with doc.create(Description()) as item:

                            if isinstance(QnA_module.question_list[i][2], dict):
                                for key, value in QnA_module.question_list[i][2].items():
                                    item.add_item('', NoEscape(f"\\hspace{{1cm}} – \\hspace{{0.25cm}} {key} - {value}"))

                            else:
                                for n in range(len(QnA_module.question_list[i][2])):
                                    item.add_item('', NoEscape(f"\\hspace{{1cm}} – \\hspace{{0.25cm}} {QnA_module.question_list[i][2][n]}"))


            with doc.create(Figure(position='H')):
                #Correction
                if QnA_module.question_list[i][5] or QnA_module.question_list[i][6]:
                    with doc.create(Subsection('Explanation :', False)) as exp:
                
                        #Correction images
                        if QnA_module.question_list[i][5]:
                            with exp.create(Center()):
                                #If multiple
                                if isinstance(QnA_module.question_list[i][5], list) or isinstance(QnA_module.question_list[i][5], tuple):
                                    with exp.create(SubFigure(position='H')) as img:
                                        for image in QnA_module.question_list[i][5]:
                                            img.add_image(image)
                                            img.append('\n')

                                else: #If only one
                                    with exp.create(SubFigure(position='H')) as img:
                                        img.add_image(QnA_module.question_list[i][5])

                        #Correction explanation
                        if QnA_module.question_list[i][6]:
                            exp.append(NoEscape(f'\n \\small {QnA_module.question_list[i][6]}'))

            doc.append(NoEscape('\\newpage'))
  

    # making a pdf using .generate_pdf
    pdf_title = 'Neurologie cellulaire'
    doc.generate_pdf(pdf_title, clean_tex=True, compiler='pdfLaTeX')

    import webbrowser
    webbrowser.open_new_tab(pdf_title + '.pdf')