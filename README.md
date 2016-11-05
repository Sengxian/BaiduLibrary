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

Or you can't switch to enter verify code manually, just leave `dmt = Node`

```Python
dmt = None
```

So when a verify code is needed, the program will save the captcha in `verifycode.png`, and you will be prompted to enter the verify code.

## Operations

Once you're log-in, you can do such things

### Sign

Sign to a specific Tieba.

```python
user.sign("kingdomrush")
```

### Get likes

Get all Tiebas that User's likes
```
user.get_likes()
```

And more operations is on the way……

