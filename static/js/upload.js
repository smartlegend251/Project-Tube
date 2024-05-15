const dropzone = document.getElementById('dropzone');
		const videoPreview = document.getElementById('video-preview');

		// Prevent default drag behaviors
		['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
		  dropzone.addEventListener(eventName, preventDefaults, false)
		  document.body.addEventListener(eventName, preventDefaults, false)
		});

		// Highlight drop zone when item is dragged over
		['dragenter', 'dragover'].forEach(eventName => {
		  dropzone.addEventListener(eventName, highlightDropzone, false)
		});

		// Remove highlight when item is dragged away
		['dragleave', 'drop'].forEach(eventName => {
		  dropzone.addEventListener(eventName, unhighlightDropzone, false)
		});

		// Handle dropped items
		dropzone.addEventListener('drop', handleDrop, false)

		function preventDefaults (e) {
		  e.preventDefault()
		  e.stopPropagation()
		}

		function highlightDropzone() {
			dropzone.classList.add('active');
		}

		function unhighlightDropzone() {
			dropzone.classList.remove('active');
		}

		function handleDrop(e) {
			const files = e.dataTransfer.files;
			if (files.length > 0) {
				const videoFile = files[0];
				const videoUrl = URL.createObjectURL(videoFile);
				videoPreview.src = videoUrl;
				videoPreview.style.display = 'block';
				dropzone.style.display = 'none';
			}
		}