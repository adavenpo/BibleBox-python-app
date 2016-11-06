$(function() {
	
	function setError(msg) {
		$('#errorMessage').css('display', 'block');
		$('#errorMessage').text(msg);
	}
	
	$("#loginForm").submit(function(e) {
		e.preventDefault();
		var usr = $('#username').val();
		var pwd = $('#password').val();

//$('#loginForm').css('display', 'none');

		$.post(
			'/app/getfilelist/', {
				'client_url': $('#client_url').val(),
				'folder_root': $('#folder_root').val(), 
				'username': usr, 
				'password': pwd
			}, 
			function(data) {
				//document.cookie = "usr=" + usr + ";path=/";
				//document.cookie = "session=" + pwd + ";path=/";
				
				$('#loginForm').css('display', 'none');
				$("#loginSubmit").prop("disabled", false);
				
				var sf = $('#selectorForm');
				
				for (var i = 0; i < data.root.length; i++) {
					var category = data.root[i][0];
					var items = data.root[i][1];
					
					sf.append($('<h3></h3>').text(category));
					var t = $('<table></table>');
					
					for (var j = 0; j < items.length; j++) {
						
						var tr = $('<tr></tr>');
						tr.append($('<td></td>').append($('<input type="checkbox"/>')));
						tr.append($('<td></td>')
							.append(
								$('<input type="hidden" />').val(items[j][1])
							).append(
								$('<input type="hidden" />').val(category)
							).append(
								$('<input type="text" size="80" />').val(items[j][0])
							)
						);
						t.append(tr);
					}
					
					sf.append(t);
				}
				
				sf.append($('<button type="submit" id="downloadButton">Download</button>'));
				$("#selectorForm").submit(downloadButtonSubmit);
			},
			'json')
		.error(function(e) {
			setError(e);
			$("#loginSubmit").prop("disabled",false);
			$("#loginSubmit").html("Submit");
		});
		
		$("#loginSubmit").prop("disabled",true);
		$("#loginSubmit").html("Loading...");
		
	});
	
	function downloadButtonSubmit(e) {
		e.preventDefault();
		
		var root = [];
		var sf = $("#selectorForm");
		
		// gather the JSON..
		
		sf.find('tr').each(function(idx, tr) {
			var inputs = $(tr).find('input');
			
			if ($(inputs[0]).prop('checked')) {
				root.push([
					$(inputs[1]).val(),
					$(inputs[2]).val(),
					$(inputs[3]).val()
				]);
			}
		});
		
		$.post(
			'/app/getcontent/',
			{
				'client_url': $('#client_url').val(),
				'username': $('#username').val(), 
				'password': $('#password').val(),
				'paths': JSON.stringify({
					root: root
				})
			}, 
			function(data) {
				$('#selectorForm').css('display', 'none');
				$('#done').text(data.status);
			},
			'json')
		.error(function(e) {
			 setError(e);
		});
		
		$("#downloadButton").prop("disabled",true);
		$("#downloadButton").html("Downloading...");
	}
});
