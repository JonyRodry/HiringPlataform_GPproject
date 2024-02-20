var save_button = document.getElementById("save-edit-button");
var delete_button = document.getElementById("delete-edit-button");
var add_comment_popup = document.getElementById("add-comment-popup")
var add_info_popup = document.getElementById("add-info-popup");
var contact_person_popup = document.getElementById("contact-person-popup");
var hiring_manager_popup = document.getElementById("hiring-manager-popup");
var change_status_popup = document.getElementById("change-status-popup");
var status_dropdown = document.getElementById("id_status");
var comments_text = document.getElementById("comments-text");
var id_comments = document.getElementById("id_comments");

function open_comments_popup(id){
    add_comment_popup.style.display = 'block';
}

function open_contactperson_popup() {

	contact_person_popup.style.display = 'block';
}

function save_contactperson_popup() {
	var contact_person_dropdown = document.getElementById("contact-person-dropdown");
	var contact_person_input = document.getElementById("contact-person-input");

	contact_person_input.value = contact_person_dropdown.options[contact_person_dropdown.selectedIndex].text;
		
	var contact_person_type = document.getElementById("contact-person-type");
	var contact_person_id = document.getElementById("contact-person-id");
	
	var type_field = document.getElementById("id_contact_person_type");
	type_field.value = contact_person_type.options[contact_person_dropdown.selectedIndex].text;
	var id_field = document.getElementById("id_contact_person_id");
	id_field.value = contact_person_id.options[contact_person_dropdown.selectedIndex].text;

	contact_person_popup.style.display = 'none';
}

function open_hiringmanager_popup() {

	hiring_manager_popup.style.display = 'block';
}

function save_hiringmanager_popup() {

	var hiring_manager_dropdown = document.getElementById("id_HiringManager");
	var hiring_manager_input = document.getElementById("hiring-manager-input");

	hiring_manager_input.value = hiring_manager_dropdown.options[hiring_manager_dropdown.selectedIndex].text;
	
	hiring_manager_popup.style.display = 'none';
}

function open_status_popup() {
	if(status_dropdown.options[status_dropdown.selectedIndex].text === 'Active')
		document.getElementById("id_pipeline_status").disabled = false;
    else
		document.getElementById("id_pipeline_status").disabled = true;

	change_status_popup.style.display = 'block';
}

function save_status_popup() {
    
	var pipeline_status_dropdown = document.getElementById("id_pipeline_status");
	var status_text = document.getElementById("status-text");
	
	if(status_dropdown.options[status_dropdown.selectedIndex].text === 'Active')
		status_text.innerHTML = status_dropdown.options[status_dropdown.selectedIndex].text + ' | ' + pipeline_status_dropdown.options[pipeline_status_dropdown.selectedIndex].text;
	else
		status_text.innerHTML = status_dropdown.options[status_dropdown.selectedIndex].text;

	change_status_popup.style.display = 'none';
}

status_dropdown.onchange = function() {
	
	if(status_dropdown.options[status_dropdown.selectedIndex].text === 'Active')
		document.getElementById("id_pipeline_status").disabled = false;
	else
		document.getElementById("id_pipeline_status").disabled = true;
}

document.onclick = function(e) {
	
    if(e.target.id !== 'contact-person-popup' && e.target.id !== 'contact-person-input' && !contact_person_popup.contains(e.target)) {
		contact_person_popup.style.display = 'none';
    }
	if(e.target.id !== 'hiring-manager-popup' && e.target.id !== 'hiring-manager-input' && !hiring_manager_popup.contains(e.target)) {
		hiring_manager_popup.style.display = 'none';
    }
	if(e.target.id !== 'change-status-popup' && e.target.className !== 'change-status-button' && !change_status_popup.contains(e.target)) {
		change_status_popup.style.display = 'none';
    }
	if(e.target.id !== 'add-comment-popup' && e.target.className !== 'add-comment-button' && !add_comment_popup.contains(e.target)) {
		add_comment_popup.style.display = 'none';
    }
};
  
function upload_documents() {
	alert("upload documents");
}

