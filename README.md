A baidu tieba Library, easy to use and Dama2 connected.

## Requirments

- python3 (requests Lib, rsa Lib)
- [Dama2 Account](http://dama2.com/)(optional)

## Getting Started

You can initialize a Tieba instance by

```python
user = Tieba("username", "password")
```

First it will check cookies in `cookies.json`(`{"BDUSS": "xxxx"}`), if it's still active, than everything is OK, or it will try to log in. In case of annoying verify code, you should first initialize your Dama2 account:

```Python
dmt = DamatuApi("username", "password")
user = Tieba("username", "password", dmt)
```

This way the program will upload the verify code to Dama2 and try to log in.

Or you can switch to enter verify code manually, just leave `dmt = None`

```Python
user = Tieba("username", "password", None)
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

### Reply

Reply to a specific post.
```python
user.reply('3986970534', "test")
```
You can also use the statement below
```python
user.reply('http://tieba.baidu.com/p/3986970534', "test content")
```

### Commit

Commit a theme post to the Tieba.
```python
user.commit('vb2012', 'test title', 'test content')
```
And more operations is on the way……

