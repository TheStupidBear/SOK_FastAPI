// сохранить токен
function saveToken(token){
 	try {
			// Сохраняем токен в localStorage с ключом 'token'
			localStorage.setItem('token', accessToken);
			console.log('Токен сохранился');
		} 
		catch (error) {
  			// Код, который выполнится при возникновении ошибки
  			console.error('Возникла ошибка:', error.message);
		}
}


// отправляем токен
async function sendTokenMain(){
	try {
		//1. Получаем токен из хранилища
		const token = localStorage.getItem('token');
		const response = await fetch('http://localhost:8000/user/me', {
    		method: 'GET',
    		headers: {
        		'Authorization': `Bearer ${token}`,
        		'Content-Type': 'application/json'
    		}
			})
		// Проверяем успешность HTTP-статуса (от 200 до 299)
    	if (!response.ok) {
        	console.error('Ошибка сервера, статус:', response.status);
        	document.getElementById('login_form').style.display = 'block';
    		document.getElementById('reg_form').style.display = 'block';
    		document.getElementById('button_exit').style.display = 'none';
    	}
        else{
        	// Превращаем ответ в объект JavaScript
    		const data = await response.json();
    		console.log(data);
    		// скрываем форму
    		document.getElementById('login_form').style.display = 'none';
    		document.getElementById('reg_form').style.display = 'none';
    		document.getElementById('button_exit').style.display = 'block';
    		document.getElementById("message").innerHTML = `Привет, ${data}`;
        }
		}
	catch (error) {
        console.error('Ошибка при запросе:', error);
    	}
 }


// отправляем токен
async function sendToken(){
	try {
		//1. Получаем токен из хранилища
		const token = localStorage.getItem('token');
		const response = await fetch('http://localhost:8000/user/me', {
    		method: 'GET',
    		headers: {
        		'Authorization': `Bearer ${token}`,
        		'Content-Type': 'application/json'
    		}
			})
		// Проверяем успешность HTTP-статуса (от 200 до 299)
    	if (!response.ok) {
        	console.error('Ошибка сервера, статус:', response.status);
    	}
        else{
        	// Превращаем ответ в объект JavaScript
    		const data = await response.json();
    		console.log(data);
        }
		}
	catch (error) {
        console.error('Ошибка при запросе:', error);
    	}
 }




// 		document.getElementById('filament_id').addEventListener('click', async (event) => {
//     	event.preventDefault();
    
//     const token = localStorage.getItem('token');
//     const targetUrl = event.target.href;

//     const response = await fetch(targetUrl, {
//         method: 'GET',
//         headers: {
//             // Префикс 'Bearer ' обязателен для работы HTTPBearer()
//             'Authorization': `Bearer ${token}` 
//         }
//     });

//     if (response.ok) {
//         const html = await response.text();
//         document.open();
//         document.write(html);
//         document.close();
//         window.history.pushState({}, '', targetUrl);
//     } else {
//         alert('Ошибка авторизации через Depends: ' + response.status);
//     }
// });



        		