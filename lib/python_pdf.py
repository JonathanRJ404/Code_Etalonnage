from datetime import date
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json 


def certificate(file_json, temperature, A, B, start, end):

        with open(file_json) as json_data:
                data_dict = json.load(json_data)
        

        Date = date.today()
        filename = "./output/CalibrationCerrtificate-"+data_dict['Device']['model']+"_"+data_dict['Device']['serial_num']+"_"+str(Date)+".pdf"

        doc = SimpleDocTemplate(filename, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        pdf = []
        ufr = "./logo/ufr.png"
        le2p = "./logo/le2p.png"
        org = "LE2P"
        operator = data_dict['operator']['firstname'] +' '+data_dict['operator']['lastname']
        pyr_model = data_dict['Device']['model']
        num_serial = data_dict['Device']['serial_num']
        reference = data_dict['Device']['reference']
        calib_period = start +' '+'-'+' '+ end
        


        style = getSampleStyleSheet()
        styleT = ParagraphStyle('title',
                                fontName="Helvetica-Bold",
                                fontSize=15,
                                parent=style['Title'],
                                alignment=TA_CENTER,
                                spaceAfter=8)

        styleH2 = ParagraphStyle('paragraph',
                                fontName="Helvetica",
                                fontSize=11,
                                parent=style['Normal'],
                                alignment=TA_LEFT,
                                spaceAfter=3)

        styleN = ParagraphStyle('paragraph',
                                fontName="Helvetica",
                                fontSize=11,
                                parent=style['Normal'],
                                alignment=TA_LEFT,
                                spaceAfter=8)

        im = Image(le2p, width=150, height=100)
        im.hAlign = 'LEFT'
        pdf.append(im)

        ptext = 'OPERATOR: %s ' % operator
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'DATE OF CERTIFICATE: %s ' % Date
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'PYRANOMETER MODEL: %s ' % pyr_model
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'SERIAL NUMBER: %s ' % num_serial
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'Reference pyranometer: %s ' % reference
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'PERIOD CALIBRATION: %s ' % calib_period
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'TEMPERATURE: %s ' % temperature
        pdf.append(Paragraph(ptext, styleH2))

        ptext = 'General consideration '
        pdf.append(Paragraph(ptext, styleT))

        ptext = 'The outdoor calibration procedure is based on a side-by-side comparison under natural sun: ' \
                'the test pyranometer  Magazine! and a reference pyranometer are mounted on a common table for horizontal ' \
                'calibration (tilt of 0°). The instruments, connected to a data logger using proper shielding are checked ' \
                'for signal and stability, their domes are cleaned. '
        pdf.append(Paragraph(ptext, styleN))

        ptext = 'Data acquisition '
        pdf.append(Paragraph(ptext, styleT))

        ptext = 'In Reunion Island, the various sky conditions may be unstable. With respects to the ' \
                'procedure which depends on the weather conditions, instantaneous voltage readings should be '\
                'simultaneously taken on both instruments at 1-mn intervals from sunrise to sunset during at least 3 weeks.  '
        pdf.append(Paragraph(ptext, styleN))

        ptext = 'Mathematical treatment '
        pdf.append(Paragraph(ptext, styleT))

        ptext = 'The reference pyranometer is of a higher class than the test pyranometer. The mathematical' \
                'treatment consists in calculating the calibration factor for each reading, which is the ratio of '\
                'the voltage measured multiplied by the calibration factor of the reference pyranometer.  '
        pdf.append(Paragraph(ptext, styleN))

        ptext = 'The final calibration factors for the test pyranometer are: '
        pdf.append(Paragraph(ptext, styleN))
        pdf.append(Paragraph('<bullet>The rain in spain</bullet>', styleN))

        ptext = 'for global radiation:   %s uV/W/m^2' % A
        pdf.append(Paragraph(ptext, styleN, bulletText='-'))
        ptext = 'for diffuse radiation:   %s uV/W/m^2' % B
        pdf.append(Paragraph(ptext, styleN, bulletText='-'))

        ptext = 'Hierarchy of traceability'
        pdf.append(Paragraph(ptext, styleT))

        ptext = 'History of calibration'
        pdf.append(Paragraph(ptext, styleT))

        data= [['', '', '', '', 'sensitivity (uV/W.m^-2)',''],
        ['date', 'operator', 'mode', 'reference', 'GHI', 'DHI']] + [[Date,data_dict['operator']['org'],data_dict['Device']['mode'],data_dict['Device']['reference'],A,B]]
        
        t=Table(data)

        t.setStyle(TableStyle([('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
        ('BOX', (0,1), (-1,-1), 0.25, colors.black),
        ('BOX', (4,0), (5,0), 0.25, colors.black),
        ('SPAN',(4,0),(5,0))
        ]))

        pdf.append(t)

        doc.build(pdf)
