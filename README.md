# Perfect World Games RPC data builder

## usage

1. use **IDE** to uncompile the game server

2. locate the target rpc function

3. copy the call list to call.dat:

```
; __unwind { // __gxx_personality_v0
push    ebp
mov     ebp, esp
sub     esp, 8
sub     esp, 8
mov     eax, [ebp+this]
push    dword ptr [eax+4] ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsEj ; GNET::Marshal::OctetsStream::operator<<(uint)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
push    dword ptr [eax+8] ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsEj ; GNET::Marshal::OctetsStream::operator<<(uint)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
add     eax, 0Ch
push    eax             ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsERKS0_ ; GNET::Marshal::OctetsStream::operator<<(GNET::Marshal const&)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
movzx   eax, byte ptr [eax+1Ch]
push    eax             ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsEh ; GNET::Marshal::OctetsStream::operator<<(uchar)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
add     eax, 20h ; ' '
push    eax             ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsERKS0_ ; GNET::Marshal::OctetsStream::operator<<(GNET::Marshal const&)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
push    dword ptr [eax+30h] ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsEi ; GNET::Marshal::OctetsStream::operator<<(int)
add     esp, 10h
sub     esp, 8
mov     eax, [ebp+this]
push    dword ptr [eax+34h] ; x
push    [ebp+os]        ; this
call    _ZN4GNET7Marshal12OctetsStreamlsEi ; GNET::Marshal::OctetsStream::operator<<(int)
add     esp, 10h
mov     eax, [ebp+os]
leave
retn
```

4. copy uncompile source codes to source.dat

```
  GNET::Marshal::OctetsStream::operator<<(os, this->capacity);
  GNET::Marshal::OctetsStream::operator<<(os, this->money);
  GNET::Marshal::OctetsStream::operator<<(os, &this->items);
  GNET::Marshal::OctetsStream::operator<<(os, this->capacity2);
  GNET::Marshal::OctetsStream::operator<<(os, &this->items2);
  GNET::Marshal::OctetsStream::operator<<(os, this->reserved1);
  GNET::Marshal::OctetsStream::operator<<(os, this->reserved2);
```

5. run

```shell
python build.py
```

6. upload the contents in result.py to WACMK server