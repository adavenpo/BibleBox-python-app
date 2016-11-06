$(function() {
	$("#loginForm").submit(function(e) {
		e.preventDefault();
		var usr = $('#userName').val();
		var pwd = $('#userPassword').val();

//$('#loginForm').css('display', 'none');

		$.post(
			'/cgi-bin/contentDownloadSelect.py', {
				'Directory': $('#directoryPath').val(), 
				'UserName': usr, 
				'UserPassword': pwd
			}, 
			function(data) {
				//document.cookie = "usr=" + usr + ";path=/";
				//document.cookie = "session=" + pwd + ";path=/";
				
				$('#loginForm').css('display', 'none');
			},
			'json')
		.error(function(e) {
			$('#errorMessage').css('display', 'block');
			$('#userName').val('');
			$('#userPassword').val('');
		});
	});
});
