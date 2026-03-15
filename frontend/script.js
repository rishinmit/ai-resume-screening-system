async function uploadFiles(event){

if(event) event.preventDefault();

try{

document.getElementById("results").innerHTML = `
<div class="loading">
<div class="loader"></div>
<p>Analyzing resumes with AI...</p>
</div>
`;

const jdFile=document.getElementById("jd").files[0];
const resumeFiles=document.getElementById("resumes").files;

const formData=new FormData();
formData.append("jd",jdFile);

for(let i=0;i<resumeFiles.length;i++){
formData.append("resumes",resumeFiles[i]);
}

const response=await fetch("http://localhost:8000/rank-resumes",{
method:"POST",
body:formData
});

const data=await response.json();

displayResults(data);

}catch(error){
console.error(error);
alert("Error occurred.");
}

}


function displayResults(data){

const ranking=data.ranking;
const names=data.resumes;

let html="";

/* STATS */

const avgScore = ranking.reduce((sum,r)=>sum+r.score,0)/ranking.length;

html += `
<div class="stats">

<div class="stat-card">
<h3>${ranking.length}</h3>
<p>Total Resumes</p>
</div>

<div class="stat-card">
<h3>${(ranking[0].score*100).toFixed(1)}%</h3>
<p>Top Score</p>
</div>

<div class="stat-card">
<h3>${(avgScore*100).toFixed(1)}%</h3>
<p>Average Score</p>
</div>

</div>
`;

/* TOP CANDIDATE */

const best=ranking[0];

html+=`
<div class="top-candidate">

<h2>⭐ Top Candidate</h2>

<p>
<a href="http://localhost:8000/files/${names[best.resume_id]}" target="_blank">
${names[best.resume_id]}
</a>
</p>

<p>Score ${(best.score*100).toFixed(2)}%</p>

<div class="score-bar">
<div class="score-fill" style="width:${best.score*100}%"></div>
</div>

</div>
`;

/* CARDS */

ranking.forEach((item,index)=>{

html+=`

<div class="card">

<h3>
Rank ${index+1} —
<a href="http://localhost:8000/files/${names[item.resume_id]}" target="_blank">
${names[item.resume_id]}
</a>
</h3>

<p>Score ${(item.score*100).toFixed(2)}%</p>

<div class="score-bar">
<div class="score-fill" style="width:${item.score*100}%"></div>
</div>

<p>Matched Skills</p>

<div class="skills matched">
${(item.matched_skills||[]).map(s=>`<span>${s}</span>`).join("")}
</div>

<p>Missing Skills</p>

<div class="skills missing">
${(item.missing_skills||[]).map(s=>`<span>${s}</span>`).join("")}
</div>

</div>

`;

});

document.getElementById("results").innerHTML=html;

}