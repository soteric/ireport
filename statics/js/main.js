var httpProto = "http://";
var domainUrl = ".successfactors.com/"

shortcut.add("Ctrl+Shift+M",function() {
	$("#jiraid").focus();
},{
	'type':'keydown',
	'propagate':true,
	'target':document
});

shortcut.add("Ctrl+Shift+U",function() {
	$("#svnid").focus();
},{
	'type':'keydown',
	'propagate':true,
	'target':document
});


function search() {
	if($("#svnid").val() !== ""){
		window.open(httpProto + "svn" + domainUrl + "viewvc/svn?view=revision&revision=" + $("#svnid").val().trim());
	}
	if($("#jiraid").val().trim() !== ""){
		document.open(httpProto + "jira" + domainUrl + "browse/" + $("#jiraid").val().trim());
	}
}