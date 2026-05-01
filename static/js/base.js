document.addEventListener("DOMContentLoaded", function () {
     function loadNavbar() {

    const user = document.body.dataset.user;
    const isAdmin = document.body.dataset.admin;

    let authHTML = "";

    if (user && isAdmin === "1") {
      // 👑 Admin
      authHTML = `
        <span class="nav-user">Hi, ${user} 👑</span>
        <a href="/admin" class="nav-admin-link">Admin</a>
        <a href="/logout" class="nav-login">Logout</a>
      `;
    } 
    else if (user) {
      // 👤 Normal user
      authHTML = `
        <span class="nav-user">Hi, ${user} 👋</span>
        <a href="/logout" class="nav-login">Logout</a>
      `;
    } 
    else {
      // 🚪 Guest
      authHTML = `
        <a href="/login" class="nav-login">Login / Register</a>
      `;
    }

    return `
      <nav>
        <div class="logo">Lumi<span>ère</span></div>

        <ul class="nav-links">
          <li><a href="/">Home</a></li>
          <li><a href="/shop">Shop</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>

        <div class="nav-right">

          <div id="nav-auth-area">
            ${authHTML}
          </div>

          <a href="/cart" class="nav-cart-btn">🛍</a>

        </div>
      </nav>
    `;
  }
    function loadFooter() {
        return `
     <!-- FOOTER -->
        <footer>
            <div class="footer-top">
                <div class="footer-brand">
                    <div class="logo">Lumi<span style="color:var(--rose); font-style:italic">ère</span></div>
                    
                    <div class="footer-socials">
                        <a class="social-btn" href="https://x.com"
                                target="_blank"
                                aria-label="Twitter" href="#">𝕏</a>
                               
                            <a
                                class="social-btn"
                                href="https://www.linkedin.com"
                                target="_blank"
                                aria-label="LinkedIn"
                                >in</a>
                        <a class="social-btn" href="https://www.instagram.com"
                                target="_blank"
                                aria-label="Instagram" href="#">📸</a>
                        <a class="social-btn" href="https://www.youtube.com"
                                target="_blank"
                                aria-label="YouTube" href="#">▶</a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>Shop</h4>
                    <ul>
                        <li>
                            <a href="#">Face Serums</a>
                        </li>
                        <li>
                            <a href="#">Moisturizers</a>
                        </li>
                        <li>
                            <a href="#">Cleansers</a>
                        </li>
                        <li>
                            <a href="#">Eye Care</a>
                        </li>
                        <li>
                            <a href="#">Bundles</a>
                        </li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Company</h4>
                    <ul>
                        <li>
                            <a href="#">Our Story</a>
                        </li>
                        <li>
                            <a href="#">Ingredients</a>
                        </li>
                        <li>
                            <a href="#">Sustainability</a>
                        </li>
                        <li>
                            <a href="#">Press</a>
                        </li>
                        <li>
                            <a href="#">Careers</a>
                        </li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Support</h4>
                    <ul>
                        <li>
                            <a href="#">FAQ</a>
                        </li>
                        <li>
                            <a href="#">Shipping & Returns</a>
                        </li>
                        <li>
                            <a href="#">Skin Quiz</a>
                        </li>
                        <li>
                            <a href="#">Contact Us</a>
                        </li>
                        <li>
                            <a href="#">Privacy Policy</a>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© 2025 Lumière Skincare. All rights reserved.</span>
                <span>Made with 💖 for every skin story.</span>
            </div>
        </footer>

    `;
    }

    document
        .getElementById("navbar")
        .innerHTML = loadNavbar();
    document
        .getElementById("footer")
        .innerHTML = loadFooter();
    document

});
