document.addEventListener('DOMContentLoaded', function () {

  function showErr(id, msg) {
    var input = document.getElementById(id);
    var err = document.getElementById(id + '-error');

    if (input) input.classList.add('error');

    if (err) {
      err.textContent = msg;
      err.classList.add('show');
    }
  }

  function clearErr(id) {
    var input = document.getElementById(id);
    var err = document.getElementById(id + '-error');

    if (input) input.classList.remove('error');
    if (err) err.classList.remove('show');
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  //  clear error live
  [
    'chk-name',
    'chk-email',
    'chk-phone',
    'chk-address',
    'chk-city',
    'chk-zip',
    'chk-country'
  ].forEach(function (id) {
    var el = document.getElementById(id);

    if (el) {
      el.addEventListener('input', function () {
        clearErr(id);
      });

      el.addEventListener('change', function () {
        clearErr(id);
      });
    }
  });

  //  submit
  document.getElementById('checkoutForm').addEventListener('submit', function (e) {

    var isValid = true;

    // 🔹 Name
    var name = val('chk-name');
    clearErr('chk-name');
    if (!name) {
      showErr('chk-name', 'Full name is required.');
      isValid = false;
    } else if (name.length < 2) {
      showErr('chk-name', 'Enter at least 2 characters.');
      isValid = false;
    }

    //  Email
    var email = val('chk-email');
    clearErr('chk-email');
    if (!email) {
      showErr('chk-email', 'Email is required.');
      isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      showErr('chk-email', 'Invalid email.');
      isValid = false;
    }

    //  Phone
    var phone = val('chk-phone');
    clearErr('chk-phone');
    var digits = phone.replace(/\D/g, '');

    if (!phone) {
      showErr('chk-phone', 'Phone required.');
      isValid = false;
    } else if (digits.length < 7 || digits.length > 15) {
      showErr('chk-phone', 'Invalid phone.');
      isValid = false;
    }

    //  Address
    var address = val('chk-address');
    clearErr('chk-address');
    if (!address) {
      showErr('chk-address', 'Address required.');
      isValid = false;
    }

    // City
    var city = val('chk-city');
    clearErr('chk-city');
    if (!city) {
      showErr('chk-city', 'City required.');
      isValid = false;
    }

    //  ZIP
    var zip = val('chk-zip');
    clearErr('chk-zip');
    if (!zip) {
      showErr('chk-zip', 'ZIP required.');
      isValid = false;
    }

    //  Country
    var country = val('chk-country');
    clearErr('chk-country');
    if (!country) {
      showErr('chk-country', 'Select country.');
      isValid = false;
    }

    
    if (!isValid) {
      e.preventDefault();

      var firstErr = document.querySelector('.form-error.show');
      if (firstErr) {
        firstErr.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      return;
    }

    

  });

});