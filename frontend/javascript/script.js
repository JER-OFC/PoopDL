// Global
const api = 'http://127.0.0.1:5000'; // Change This
// const api = 'https://poopdl-api.dapuntaratya.com'; // Change This

// Global variable
let list_file;

// Add Event Listener Submit Button
const inputForm = document.getElementById('poop_url');
const submitButton = document.getElementById('submit_button');
submitButton.addEventListener('click', (event) => {
    const url = inputForm.value;
    readInput(url);
});

// Loading Spinner 1
function loading(element_id, active) {
    const loadingBox = document.getElementById(element_id);
    if (active)  {
        loadingBox.innerHTML = `<div id="loading-spinner" class="spinner-container"><div class="spinner"></div></div>`;
        loadingBox.style.pointerEvents = 'all';
    }
    else {
        loadingBox.innerHTML = `Fetch`;
        loadingBox.style.pointerEvents = 'all';
    }
}

// Loading Spinner 2
function loading2(element_id, active) {
    const loadingBox = document.getElementById(element_id);
    if (active)  {
        loadingBox.innerHTML = `<div id="loading-spinner" class="spinner-container"><div class="spinner2"></div></div>`;
        loadingBox.style.pointerEvents = 'all';
    }
    else {
        loadingBox.innerHTML = `Failed`;
        loadingBox.style.pointerEvents = 'all';
    }
}

// Loading Spinner 3
function loading3(element_id, active) {
    const loadingBox = document.getElementById(element_id);
    if (active)  {
        loadingBox.innerHTML = `<div id="loading-spinner" class="spinner-container"><div class="spinner2"></div></div>`;
        loadingBox.style.pointerEvents = 'none';
    }
    else {
        loadingBox.innerHTML = `<i class="fa-solid fa-play"></i>`;
        loadingBox.style.pointerEvents = 'auto';
    }
}

// Time Sleep
function sleep(s) {
    return new Promise(resolve => setTimeout(resolve, s*1000));
}

// Read Input
async function readInput(raw_url) {

    const list_url = raw_url.replace(/\n/g, "").replace(/\s/g, '') === '' ? null : raw_url.split("\n");;

    if (list_url) {
        list_file = [];
        params = {};
        document.getElementById('result').innerHTML = '';
        loading('submit_button', true);
        
        for (const item of list_url) {
            const url = item.trim();
            await fetchURL(url);
        }

        loading('submit_button', false);
        inputForm.value = '';
    }

    else {
        loading('submit_button', false);
        inputForm.value = '';
    }

    if (list_file.length == 0) {
        errorFetch();
    }

}

// Fetch URL
async function fetchURL(url) {

    try {

        const get_file_url = `${api}/generate_file`;
        const headers = {'Content-Type':'application/json'};
        const data = {
            'method'  : 'POST',
            'mode'    : 'cors',
            'headers' : headers,
            'body'    : JSON.stringify({'url':url})
        };

        const req = await fetch(get_file_url, data);
        const response = await req.json();

        if (response.status == 'success') {
            await printItem(response.file);
        }

    }

    catch (e) {
        console.log(e);
    }
}

// Error Fetch
function errorFetch() {
    const box_result = document.getElementById('result');
    box_result.innerHTML = `
        <div class="container-failed">
            <span>Fetch Failed</span>
        </div>`;
}

// Show Item
async function printItem(response) {

    const box_result = document.getElementById('result');

    response.forEach((item) => {
        list_file.push(item);
        const new_element = document.createElement('div');
        new_element.id = `file-${item.id}`;
        new_element.className = 'container-item';
        new_element.innerHTML = `
            <div class="container-item-default">
                <div id="image-${item.id}" class="container-image"><img src="${item.image}" onclick="zoom(this)"></div>
                <div class="container-info">
                    <span id="title-${item.id}" class="title">${item.name}</span>
                    <div class="container-button">
                        <div id="container-download-${item.id}" class="container-download-button">
                            <button id="get-download-${item.id}" type="button" class="download-button">Download</button>
                        </div>
                        <div class="container-stream-button-valid">
                            <button id="stream-${item.id}" type="button" class="stream-button"><i class="fa-solid fa-play"></i></button>
                        </div>
                    </div>
                </div>
            </div>
            <div id="video-box-${item.id}" class="container-item-expand false">
            </div>`;
        box_result.appendChild(new_element);

        const downloadButton = new_element.querySelector(`#get-download-${item.id}`);
        downloadButton.addEventListener('click', () => {
            initDownload(item.domain, item.id);
        });

        const streamButton = new_element.querySelector(`#stream-${item.id}`);
        streamButton.addEventListener('click', () => {
            initStream(item.domain, item.id);
        });
    });
}

// Initialization for download
async function initDownload(domain, id) {

    loading2(`get-download-${id}`, true);

    const param = {'domain':domain, 'id':id};

    const get_link_url = `${api}/generate_link`;
    const headers = {'Content-Type':'application/json'};
    const data = {
        'method'  : 'POST',
        'mode'    : 'cors',
        'headers' : headers,
        'body'    : JSON.stringify(param)
    };

    const req = await fetch(get_link_url, data);
    const response = await req.json();

    if (response.status == 'success') {
        startDownload(response.link);
        document.getElementById(`get-download-${id}`).innerHTML = 'Download';
    }

    else {
        loading2(`get-download-${id}`, false);
    }
}

// Start Download
async function startDownload(url) {
    window.open(url, '_blank', 'noopener,noreferrer');
}

// Initialization for stream
async function initStream(domain, id) {
    const expanded_box = document.getElementById(`file-${id}`);
    const video_box = document.getElementById(`video-box-${id}`);

    if (expanded_box.className == 'container-item') {
        const source_vid = document.getElementById(`video-box-${id}`);
        if (source_vid.innerHTML.replace(/\s/g, '') === '') {

            loading3(`stream-${id}`, true);
            const url_stream = await getURLStream(domain, id);
            source_vid.innerHTML = `
                <video controls>
                    <source id="stream-video-${id}" src="${url_stream}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>`;
            // source_vid.innerHTML = `<video id="video" controls width="600" height="400" src="${url_stream}"></video>`;
            loading3(`stream-${id}`, false);

        }
        expanded_box.className = 'container-item expand';
        video_box.className = 'container-item-expand';
    }
    else {
        expanded_box.className = 'container-item';
        video_box.className = 'container-item-expand false';
    }
}

// Get URL Stream
async function getURLStream(domain, id) {

    try {
        
        const param = {'domain':domain, 'id':id};

        const get_link_url = `${api}/generate_link`;
        const headers = {'Content-Type':'application/json'};
        const data = {
            'method'  : 'POST',
            'mode'    : 'cors',
            'headers' : headers,
            'body'    : JSON.stringify(param)
        };
    
        const req = await fetch(get_link_url, data);
        const response = await req.json();

        if (response.status == 'success') return(response['link']);
        else return('');
    }
    catch {return('');}
}