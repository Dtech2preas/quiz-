const fs = require('fs');
const quizHtml = fs.readFileSync('quiz.html', 'utf8');
const dashboardHtml = fs.readFileSync('dashboard.html', 'utf8');
console.log('Quiz contains #certificate-template?', quizHtml.includes('id="certificate-template"'));
console.log('Dashboard contains #report-card-template?', dashboardHtml.includes('id="report-card-template"'));
