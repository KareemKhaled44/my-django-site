🛒 Supplement Store – E-commerce Web App
This is a full-featured e-commerce platform built with Django and TailwindCSS for a supplement store. The website supports user-friendly shopping, real-time interactivity with AJAX, a dedicated user dashboard, and a built-in accounting system to help store owners manage their finances efficiently.
Users can browse and search for products, add them to their cart or wishlist, proceed to checkout with various payment methods, and track their orders.

🚀 Features

🛒 Shopping & Product Features
- Product listing with AJAX-based filters, pagination, and add to cart (no page reloads).

- Product detail pages with dynamic related products from the same category.

- Search functionality to find products easily.

- Display of Best Sellers and New Arrivals on the homepage (based on business logic).

💳 Checkout & Orders
- Checkout page with address selection, payment method (Cash on Delivery & Vodafone Cash).

- Order tracking: users can view their full order history and details.

- Cart management with real-time updates.

👤 User Dashboard
- Orders: full order history with details.

- Wishlist: add/remove favorite products using AJAX.

- Addresses: add, update, delete addresses, and set a default one (used in autofill at checkout).

Account Details: view/update name & email, and change password securely.

🔐 Authentication & Security
- User registration & login system.

- Password reset (Forget Password) feature.

- Contact form available only for authenticated users.


📊 Admin Dashboard & Reporting
🧾 Dashboard Overview
Summary cards showing:

Total Orders

Total Revenue

Total Paid Orders

Total Products

Total Profit

Monthly Earnings

Latest 5 orders displayed with quick access.

Quick actions for navigating or managing common admin tasks.

📈 Analytics (powered by Chart.js)
Orders Trend (last 3 months) – bar chart showing number of orders per month.

Stock Status – comparison chart between in-stock and out-of-stock products.

Revenue Trend – line chart showing revenue per month.

Top Products by Revenue – bar chart showing top-earning products.

📚 Admin Pages (via Django Admin)
Manage all key data through Django Admin:

Products

Orders

Customers

Categories

Brands, etc.

Includes store settings like:

Change admin email and password

Configure general preferences

📑 Reports & Accounting
Downloadable Excel reports:

Sales Report

Monthly Report (date range filterable)

Top Selling Products

Balance Sheet showing:

Assets (e.g. paid revenue, receivables)

Liabilities (e.g. unpaid orders)

Net Worth (assets - liabilities)

All financial data computed based on actual paid orders and product-level profits.

💡 Extra Features
- Built-in accounting system for tracking profits and generating financial data.

- Admin can control product stock, categories, and brands.

- The entire site is fully responsive and mobile-friendly.

- Designed with TailwindCSS for a modern, clean interface.
