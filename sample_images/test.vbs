Dim barcode 

Set barcode = WScript.CreateObject("LibBridgeT.Barcode")

barcode.Symbology = 10

Dim result

On Error Resume Next

result = barcode.ReadBarcodes("E:\Tecnomedia\image-viewer\sample_images\resultado_BN_DINA4.tif" )

If Err.Number <> 0 Then
	MsgBox Err.Description
	Err.Clear
End If

MsgBox "Después"

Msgbox result

Dim bars
Dim syms

set bars = barcode.ResultBars
set syms = barcode.ResultSyms

If Ubound(bars) + 1 > 0 Then
	
	for i = 0 To Ubound(bars)
		Msgbox bars(i)
	next

End If


ErrorCatch:
MsgBox "Error"