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












        		