import React, {useEffect, useState} from 'react';
import { Cookies } from 'react-cookie';
import OrderItem from "./order_item";
import Ticker from "./ticker";


function OrderPage(props) {
    // test func
    function sendUpdateRequest() {
        // Choose a random symbol and price
        // const symbols = ['BTC', 'ETH', 'RUB', 'USD', 'BNB'];
        const symbols = ['RUB'];
        const symbol = symbols[Math.floor(Math.random() * symbols.length)];
        const price = Math.floor(Math.random() * 991) + 10;

        // Construct the request body
        const requestBody = {
            symbol: symbol,
            current_price: price
        };

        // Send the request using the fetch API
        fetch('http://127.0.0.1:8000/assets/updateasset/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to send update request');
                }
                console.log('Update request sent successfully');
            })
            .catch(error => {
                console.error(error);
            });
    }
    setInterval(sendUpdateRequest, 10000);
    // test func



    const cookies = new Cookies();
    const [ordersData,setOrdersData] = useState([])

    function verify_token() {
        const tokenData = {
            token: cookies.get('access_token'),
        };
        fetch('http://127.0.0.1:8000/api/auth/jwt/verify/', {
            method: 'POST',
            body: JSON.stringify(tokenData),
            headers: {
                'Content-Type': 'application/json',
            }

        })
            .then(response => {
                if (response.status === 200) {
                    return true;
                } else {
                    window.location.href = '/auth';
                    return false;
                }
            })
            .catch(error => {
                console.error('Error verifying token:', error);
                return false;
            });
    }


    useEffect(()=> {
        if (!cookies.get('access_token')) {
            const nextPageUrl = '/auth';
            window.location.replace(nextPageUrl);
        } else {
            verify_token()
                const socket = new WebSocket("ws://127.0.0.1:8000/ws/orders/?token=" + cookies.get('access_token'));
                socket.onmessage = function (event) {
                    const data = JSON.parse(event.data);
                    if (data.message.messageText === 'GetOrder') {
                        setOrdersData(ordersData => ordersData = data.message.orders)
                    } else if (data.message.messageText === 'OrderUpdated') {
                        setOrdersData(prevOrdersData => {
                            const updatedOrdersData = prevOrdersData.map(order => {
                                if (data.message.order.id === order.id) {
                                    return data.message.order;
                                } else {
                                    return order;
                                }
                            });
                            return updatedOrdersData;
                        });
                    } else if (data.message.messageText === 'PlaceOrder') {
                        setOrdersData(prevOrdersData => [...prevOrdersData, data.message.order]);
                    }
                };
            }
    },[])

    if (ordersData)
    return (
        <>
            <Ticker/>
        <div className="content">
            <div className="container">
                <h2 className="mb-5">My Orders</h2>
                <button type="button" className="btn btn-primary create" data-toggle="modal" data-target="#exampleModalCenter">
                    Create Order
                </button>
                <div className="table-responsive custom-table-responsive">
                    <table className="table custom-table">
                        <thead>
                        <tr>
                            <th scope="col">
                        </th>
                        <th scope="col">ID</th>
                        <th scope="col">Creation time</th>
                        <th scope="col">Change time</th>
                        <th scope="col">Status</th>
                        <th scope="col">Side</th>
                        <th scope="col">Price</th>
                        <th scope="col">Amount</th>
                        <th scope="col">Instrument</th>
                        </tr>
                    </thead>
                    <tbody>
                    {ordersData.map((order, index) => {
                        return <OrderItem key={index+1} order={order}/>
                    })}
                    </tbody>
                </table>
            </div>
        </div>
</div>
        </>
    );
}

export default OrderPage;