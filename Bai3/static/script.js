function openSidebar() {
    document.getElementById("sidebar").style.width = "250px";
}

function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";
}
function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const passwordIcon = document.getElementById('togglePassword');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';  // Thay đổi thành text để hiện mật khẩu
        passwordIcon.innerHTML = '🙈';  // Thay đổi biểu tượng thành 'ẩn' (hoặc bất kỳ biểu tượng nào bạn muốn)
    } else {
        passwordField.type = 'password';  // Thay lại kiểu password
        passwordIcon.innerHTML = '👁️';  // Thay lại biểu tượng 'hiển thị' mật khẩu
    }
}
function hidePasswordIcon() {
    const passwordIcon = document.getElementById('togglePassword');
    passwordIcon.style.display = 'none';  // Ẩn biểu tượng mà không ảnh hưởng đến input
}


// Hiển thị lại icon khi người dùng bỏ focus (không nhập nữa)
document.getElementById('password').addEventListener('blur', function() {
    document.getElementById('togglePassword').style.display = 'inline-block';  // Hiển thị lại icon khi người dùng không focus vào input
});

