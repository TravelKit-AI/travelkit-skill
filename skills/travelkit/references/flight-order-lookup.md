# flight-order-lookup ref

## flight_order_detail / flight_order_detail_by_external_id / flight_order_list

查询用户的机票订单状态和订单列表。

### 工具选择

| 场景 | 使用工具 |
|------|---------|
| 用户提供 TravelKit 订单号 | `flight_order_detail` |
| 用户提供买方侧外部订单号 | `flight_order_detail_by_external_id` |
| 用户查找历史订单、按路线/日期/状态/票号/航司 PNR 筛选 | `flight_order_list` |

**始终通过工具获取最新状态**，不依赖记忆中的出票、付款、退款或改签状态。

### 订单详情展示

展示订单状态时，以普通语言摘要以下内容：

- 订单号
- 乘客姓名（数据返回时）
- 航线和航班段
- 支付状态
- 出票状态
- 下一步可用操作

### 订单列表展示

`flight_order_list` 返回多条结果时：

- 按出发日期排序展示
- 每条显示：订单号、路线、出发日期、支付状态、出票状态
- 说明用户可以指定某个订单号继续操作

### 错误处理

订单找不到时，询问：订单号、外部订单号、票号、路线或出发日期，从而帮助定位。
