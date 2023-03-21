import React, {useEffect, useState} from 'react';
import { Cookies } from 'react-cookie';
import OrderItem from "./order_item";


function OrderPage(props) {
    const cookies = new Cookies();
    const [ordersData,setOrdersData] = useState([])

    useEffect(()=> {
        if (!cookies.get('access_token')) {
            const nextPageUrl = '/auth';
            window.location.replace(nextPageUrl);
        } else {
            const socket = new WebSocket("ws://127.0.0.1:8000/ws/orders/?token="+cookies.get('access_token'));
            socket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.message.messageText === 'GetOrder'){
                    setOrdersData(ordersData => ordersData = data.message.orders)
                } else if (data.message.messageText === 'OrderUpdated'){
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
                    setOrdersData([...ordersData, data.message.order])
                }
            };
        }
    },[])

    if (ordersData)
    return (
        <div class="content">
            <div class="container">
                <h2 class="mb-5">My Orders</h2>
                <button type="button" class="btn btn-primary create" data-toggle="modal" data-target="#exampleModalCenter">
                    Create Order
                </button>
                <div class="table-responsive custom-table-responsive">
                    <table class="table custom-table">
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
                    {ordersData.map((order) => {
                        return <OrderItem order={order}/>
                    })}
                    </tbody>
                </table>
            </div>
        </div>
</div>
    );
}

export default OrderPage;