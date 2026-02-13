const audio=document.getElementById("audio");
const list=document.getElementById("list");

fetch("/tracks")
.then(r=>r.json())
.then(tr=>{
    tr.forEach(t=>{
        let o=document.createElement("option");
        o.value=t.file;
        o.text=t.name;
        list.appendChild(o);
    });
});

list.onchange=e=>{
    audio.src="/stream/"+e.target.value.split("/").pop();
};
