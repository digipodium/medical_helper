console.log('loaded rent js')

fetch('/config/')
.then((result) =>{
    return result.json();
})
.then((data)=>{
    const stripe = Stripe(data.publicKey)
    
    document.querySelector('#rentbtn').addEventListener('click',()=>{
        var amt = parseFloat(document.querySelector(".amount>span>b").innerHTML)
        fetch('/create-rent-session/?price='+amt)
        .then((result)=>{return result.json();})
        .then((data)=>{
            console.log(data);
            return stripe.redirectToCheckout({sessionId:data.sessionId})
        }).
        then((res)=>{
            console.log(res)
        })
    });
});