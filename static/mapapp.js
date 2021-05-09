const submit = document.querySelector("#submit");
submit.addEventListener("click", function (e) {
	e.preventDefault();
	const modal = document.querySelector(".modal");
	modal.style.display = "flex";
});

const closeModal = document.querySelector(".modal__exit");
closeModal.addEventListener("click", function () {
	const modal = document.querySelector(".modal");
	modal.style.display = "none";
});

const confirm = document.querySelector(".submit-confirm");
confirm.addEventListener("click", function (e) {
	e.preventDefault();
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
