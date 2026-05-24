const API_URL = "http://127.0.0.1:8000";

function openAndDownloadResume(filename){
const encodedName = encodeURIComponent(filename);
window.open(`${API_URL}/files/${encodedName}`, "_blank");

const downloadLink = document.createElement("a");
downloadLink.href = `${API_URL}/download/${encodedName}`;
downloadLink.download = filename;
downloadLink.style.display = "none";
document.body.appendChild(downloadLink);
downloadLink.click();
downloadLink.remove();
}

async function uploadFiles(event){

if(event) event.preventDefault();

try{
const resultsEl = document.getElementById("results");
const button = document.querySelector("button");
const jdFile=document.getElementById("jd").files[0];
const resumeFiles=document.getElementById("resumes").files;

if(!jdFile){
resultsEl.innerHTML = `<div class="card"><p>Please select a job description file.</p></div>`;
return;
}

if(!resumeFiles || resumeFiles.length === 0){
resultsEl.innerHTML = `<div class="card"><p>Please select at least one resume file.</p></div>`;
return;
}

resultsEl.innerHTML = `
<div class="loading">
<div class="loader"></div>
<p>Analyzing resumes with AI...</p>
</div>
`;
resultsEl.scrollIntoView({ behavior: "smooth", block: "start" });
if(button) button.disabled = true;

const formData=new FormData();
formData.append("jd",jdFile);

for(let i=0;i<resumeFiles.length;i++){
formData.append("resumes",resumeFiles[i]);
}

// const response=await fetch("http://localhost:8000/rank-resumes",{
const response = await fetch(`${API_URL}/rank-resumes`,{
method:"POST",
body:formData
});

if(!response.ok){
throw new Error(`Backend returned ${response.status}`);
}

const data=await response.json();
console.log("Resume ranking response:", data);

displayResults(data);

}catch(error){
console.error(error);
document.getElementById("results").innerHTML = `
<div class="card">
<h3>Analysis failed</h3>
<p>Make sure the backend is running at ${API_URL} and try again.</p>
<p>${error.message}</p>
</div>
`;
}finally{
const button = document.querySelector("button");
if(button) button.disabled = false;
}

}


function displayResults(data){

const ranking=data.ranking;
const names=data.resumes;

if(!ranking || ranking.length === 0){
document.getElementById("results").innerHTML = `
<div class="card">
<h3>No results found</h3>
<p>The backend did not return any ranked resumes.</p>
</div>
`;
return;
}

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

{/* <a href="http://localhost:8000/files/${names[best.resume_id]}" target="_blank"></a> */}
html+=`
<div class="top-candidate">

<h2>⭐ Top Candidate</h2>

<p>

<a href="#" onclick="openAndDownloadResume('${names[best.resume_id].replace(/'/g, "\\'")}'); return false;">
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
{/* <a href="http://localhost:8000/files/${names[item.resume_id]}" target="_blank"></a> */}
ranking.forEach((item,index)=>{

html+=`

<div class="card">

<h3>
Rank ${index+1} —

<a href="#" onclick="openAndDownloadResume('${names[item.resume_id].replace(/'/g, "\\'")}'); return false;">
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
document.getElementById("results").scrollIntoView({ behavior: "smooth", block: "start" });

}
