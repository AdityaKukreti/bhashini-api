import requests

print(requests.post("http://127.0.0.1:10000/getLikenessAndIntent", json = {'conversation':"""
Buyer: Hi there! I've been looking for a new smartphone. My current one
is starting to give me trouble. Any recommendations?

Seller: Absolutely! I can help you find the perfect phone. What features
are most important to you? Budget, camera quality, battery life, or
something else?

Buyer: Good question. For now, my main priority is a long-lasting battery
and good value for money. Something under $500 would be great too.

Seller: I have just the phone in mind then! The XYZ Smartphone has an
impressive 48-hour battery life on average and offers excellent
performance at a price point of around $450, which is well within your
budget.

Buyer: That sounds promising. Can you tell me more about its camera
quality? I like taking photos when I'm out with friends.

Seller: Of course! The XYZ Smartphone comes equipped with a 12-MP rear
camera and an 8-MP front camera, which should provide great image quality
for your social gatherings. It also supports HDR imaging for more vibrant
photos.

Buyer: Sounds good so far. How's the overall performance? And what about
customer service if I encounter any issues with my new phone?

Seller: The XYZ Smartphone runs on a powerful processor and comes with 4GB
RAM, ensuring smooth multitasking and fast app launches. As for customer
service, we have an excellent support team ready to assist you at all
times. Plus, the warranty covers any potential issues within one year of
purchase.

Buyer: Excellent! I'll take it. What payment methods do you accept?

Seller: We accept major credit cards and mobile payment options like Apple
Pay or Google Wallet. Which option would work best for you?

Buyer: Credit card will be fine. Let me grab my wallet, and we can
complete the transaction then.

Seller: Fantastic! Once we've processed your purchase, I'll have a box
ready with everything you need to set up your new XYZ Smartphone. Have a
great day, and enjoy your new phone!

"""}).json())