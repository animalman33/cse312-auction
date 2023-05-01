function onload() {
    let request = new XMLHttpRequest();

    request.onreadystatechange = function() {
	if (this.readyState === 4 && this.status === 200) {
	    data = JSON.parse(this.response)

	    for (x of data) {
		document.getElementsByName('auctions') += "" ;
	    }
	}
    }

    request.open('GET', "/user/auc")
    request.send();
}
