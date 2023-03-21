import React from 'react';

function OrderItem(props) {
    return (
        <tr scope="row">
            <th scope="row">
                <label className="control control--checkbox">
                    <input type="checkbox"></input>
                    <div className="control__indicator"></div>
                </label>
            </th>

            <td>
                {props.order.id}
            </td>

            <td>
                {props.order.order_status}
            </td>

            <td>
                {props.order.id}
            </td>

            <td>{props.order.id}</td>
            <td>{props.order.id}</td>
            <td>{props.order.id}</td>
            <td>{props.order.id}</td>
            <td>{props.order.id}</td>
        </tr>
    );
}

export default OrderItem;