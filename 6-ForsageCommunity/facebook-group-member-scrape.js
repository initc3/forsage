/*
* Facebook Group Member Scrape: copy this into your dev console in chrome or FF
* on a website like:
* https://m.facebook.com/browse/group/members/?id=redacted&start=0&listType=list_nonfriend_nonadmin&ref=group_browse
*/

/**
* console-save.js #  
* (view raw)
* 
* A simple way to save objects as .json files from the console, includes a chrome extension along with a plain script.
* Usage
* 
* console.save(data, [filename])
* 
* Data can be a string or just an object, objects are passed through json.stringify() before writing to file. Filename is optional, defaults to ‘console.json’.
* Licence
* 
* MIT
* http://bgrins.github.io/devtools-snippets/#console-save
*/
(function(console){

    console.save = function(data, filename){

        if(!data) {
            console.error('Console.save: No data')
            return;
        }

        if(!filename) filename = 'console.json'

        if(typeof data === "object"){
            data = JSON.stringify(data, undefined, 4)
        }

        var blob = new Blob([data], {type: 'text/json'}),
            e    = document.createEvent('MouseEvents'),
            a    = document.createElement('a')

        a.download = filename
        a.href = window.URL.createObjectURL(blob)
        a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
        e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
        a.dispatchEvent(e)
    }
})(console)

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

//var class_attr = "._55wr _7om2 _5b6o touchable _592p _25mv";
//var class_attr = "._55wr"; //mobile facebook
var class_attr = ".oajrlxb2"; //www facebook

var people = document.querySelectorAll(class_attr);
var count = people.length;
var people_set = new Set();

var trip_counter = 0;

async function doScrape() {
//    while (trip_counter < 10) {
    while (people_set.size < 9999) {
        people = document.querySelectorAll(class_attr);
        let new_count = people.length;
        let people_set_size = people_set.size;
        if ( new_count === count ) {
            console.log(`No new people, incrementing trip_counter ${trip_counter} Set size ${people_set_size}`);
            window.scrollBy(0,getRandomInt(250,800));
            await sleep(getRandomInt(1000,5000));
            trip_counter++;
        } else {
            console.log(`New people. Set size ${people_set_size}`);
            count = new_count;
            trip_counter = 0;
            for (let i = 0; i < people.length; i++) {
                //person_id = JSON.stringify(people[i].id); // mobile
                person_id = JSON.stringify(people[i].href); // www
                if(!people_set.has(person_id)){
                    console.log(person_id);
                    people_set.add(person_id);
                }
            }
        }
    }
    console.log("Done.");
}
doScrape();
console.save(Array.from(people_set));



// var profile_id = "redacted"
// var user_id_prefix = `https://m.facebook.com/profile.php?id=${profile_id}&sk=about`
