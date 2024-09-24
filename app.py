from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        absents = int(request.form['absences'])
        prelexgrade = float(request.form['prelexgrade'])
        quizgrad = float(request.form['quizgrad'])
        reqgrade = float(request.form['reqgrade'])
        recigrade = float(request.form['recigrade'])

        if prelexgrade < 0 or prelexgrade > 100 or quizgrad < 0 or quizgrad > 100 or \
            reqgrade < 0 or reqgrade > 100 or recigrade < 0 or recigrade > 100:
            return "Please enter valid grades between 0 and 100."

        attendance = 100 - (absents * 10)
        if absents >= 4:
            return render_template('failed.html')
        
        attendance = max(attendance, 0)

        classstand = (quizgrad * 0.40) + (reqgrade * 0.30) + (recigrade * 0.30)
        
        prelimgrade = (prelexgrade * 0.60) + (attendance * 0.10) + (classstand * 0.30)

        def calculate_required_grades(prelim_grade, target):
            remaining = target - (0.20 * prelim_grade)
            midterm_needed = remaining / (0.30 + 0.50)
            final_needed = midterm_needed
            return midterm_needed, final_needed

        midterm_needed_75, final_needed_75 = calculate_required_grades(prelimgrade, 75)
        midterm_needed_90, final_needed_90 = calculate_required_grades(prelimgrade, 90)
        
        return render_template('result.html', prelimgrade=prelimgrade,
                               midterm_needed_75=midterm_needed_75, final_needed_75=final_needed_75,
                               midterm_needed_90=midterm_needed_90, final_needed_90=final_needed_90)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
