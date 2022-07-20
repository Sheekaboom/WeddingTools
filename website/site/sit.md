---
layout: default
title: Sit
---

# hey party people !

Enter your name to find your table number. If you're unsure you're at the right table, the table markers have the names of everyone at that table. 

Take any seat at your table - you won't be in it for long!

<script type="module">
    import {Autocomplete} from '/js/autocomplete.js';
    import seating_data from '/data/sit_data.json' assert {type: 'json'};

    var input = document.querySelector('#lname');
    var name_list = document.querySelector('#name_list');
    var name_temp = name_list.getElementsByTagName('template')[0];
    var table_number = document.querySelector('#table_number');
    var ac = new Autocomplete(seating_data);

    function set_table_number(e) {
        var person_data = seating_data[e.target.innerText];
        table_number.innerText = person_data['table'].toString();
    }

    function autocomplete_seating() {
        var matches = ac.query(input.value);
        name_list.innerHTML = '';
        for (let m in matches) {
            var name_item = document.createElement('li');
            name_item.addEventListener('click', set_table_number);
            name_item.setAttribute("class",".name_item");
            name_item.innerText = m
            name_list.appendChild(name_item);
        }
    }
    
    input.addEventListener('input',autocomplete_seating);
</script>

<form>
    <!--label for="fname">First name:</label><br>
    <input type="text" id="fname" name="fname"><br-->
    <!--label for="lname">Name</label><br-->
    <input type="text" id="lname" name="lname" placeholder='Name'>
</form>

<div id='name_select_info'>select your name from the list:</div>

<ul id="name_list">
    <template><li style=".person_select"></li></template>
</ul>

<div id="table_number" style="font-size: xx-large;"></div>