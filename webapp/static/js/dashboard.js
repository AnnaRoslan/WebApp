async function send($this) {

    var formData = new FormData();
    var url = window.location.href
    var id = $this.id;
    formData.append("id", id);
    var request = new XMLHttpRequest();
    request.open("DELETE", url);
    request.send(formData);

}