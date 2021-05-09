const send = document.querySelector("#submit");
send.addEventListener("click", function (e) {
	e.preventDefault();
	console.log("dss");
	sendEmail(true);
});
function sendEmail(positive) {
	console.log("start");

	let templateParams = { to_name: "Albert" };
	if (positive === true) {
		emailjs
			.send(
				"service_9ddwxzs",
				"template_wmbwup2",
				templateParams,
				"user_dG1pOTK50id2f9RL6qaDz"
			)
			.then(
				function (response) {
					console.log("SUCCESS!", response.status, response.text);
				},
				function (error) {
					console.log("FAILED...", error);
				}
			);
	} else {
		emailjs.send(
			"service_9ddwxzs",
			"template_jyqxlwo",
			templateParams,
			"user_dG1pOTK50id2f9RL6qaDz"
		);
	}
}
