A baidu tieba Library, easy to use and Dama2 connected.

## Requirments

- python3
- [Dama2 Account](http://dama2.com/)(optional)

## Getting Started

You can initialize a Tieba instance by

```python
user = Tieba("username", "password")
```

First it will check cookies in `cookies.json`(`{"BDUSS": "xxxx"}`), if it's still active, than everything is OK, or it will try to log in. In case of annoying verify code, you should first initialize your Dama2 account:

```Python
dmt = DamatuApi("username", "password")
```

This way the program will upload the verify code to Dama2 and try log in.

When you're log-in, you can sign to a specific tieba

```python
user.sign("kingdomrush")
```

And more operations is on the way……

