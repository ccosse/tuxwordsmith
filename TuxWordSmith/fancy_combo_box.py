import wx,os
DEBUG=0

class NullLog:
    def write(*args):
        if DEBUG:print args[1]

class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):
        
    def __init__(self, callback, log=None):
        self.callback=callback
        if log:
            self.log = log
        else:
            self.log = NullLog()
            
        
        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())

        # Also init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)
        

    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            self.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.


    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.log.write("ListCtrlComboPopup.Init")
        self.value = -1
        self.curitem = -1


    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.log.write("ListCtrlComboPopup.Create")
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        #self.log.write("ListCtrlComboPopup.GetControl")
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        self.log.write("ListCtrlComboPopup.SetStringValue")
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)
        #self.callback(None)

    # Return a string representation of the current item.
    def GetStringValue(self):
        self.log.write("ListCtrlComboPopup.GetStringValue")
        if self.value >= 0:
            return self.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        self.log.write("ListCtrlComboPopup.OnPopup")
        wx.combo.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        self.log.write("ListCtrlComboPopup.OnDismiss")
        wx.combo.ComboPopup.OnDismiss(self)
        self.callback(None)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        self.log.write("ListCtrlComboPopup.PaintComboControl")
        wx.combo.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        self.log.write("ListCtrlComboPopup.OnComboKeyEvent")
        wx.combo.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        self.log.write("ListCtrlComboPopup.OnComboDoubleClick")
        wx.combo.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        self.log.write("ListCtrlComboPopup.GetAdjustedSize: %d, %d, %d" % (minWidth, prefHeight, maxHeight))
        return wx.combo.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.    
    # Default returns false.
    def LazyCreate(self):
        self.log.write("ListCtrlComboPopup.LazyCreate")
        return wx.combo.ComboPopup.LazyCreate(self)
    

CUSTOM_COMBOBOX_ANIMATION_DURATION = 200
class ComboCtrlWithCustomPopupAnim(wx.combo.ComboCtrl):
    def __init__(self, *args, **kw):
        wx.combo.ComboCtrl.__init__(self, *args, **kw)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.aniTimer = wx.Timer(self)


    def AnimateShow(self, rect, flags):
        self.aniStart = wx.GetLocalTimeMillis()
        self.aniRect = wx.Rect(*rect)
        self.aniFlags = flags

        dc = wx.ScreenDC()
        bmp = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.MemoryDC(bmp)
        if "wxMac" in wx.PlatformInfo:
            pass
        else:
            mdc.Blit(0, 0, rect.width, rect.height, dc, rect.x, rect.y)
        del mdc
        self.aniBackBitmap = bmp

        self.aniTimer.Start(10, wx.TIMER_CONTINUOUS)
        self.OnTimer(None)
        return False
        

    def OnTimer(self, evt):
        stopTimer = False
        popup = self.GetPopupControl().GetControl()
        rect = self.aniRect
        dc = wx.ScreenDC()

        if self.IsPopupWindowState(self.Hidden):
            stopTimer = True
        else:
            pos = wx.GetLocalTimeMillis() - self.aniStart
            if pos < CUSTOM_COMBOBOX_ANIMATION_DURATION:
                # Actual animation happens here
                width = rect.width
                height = rect.height

                center_x = rect.x + (width/2)
                center_y = rect.y + (height/2)

                dc.SetPen( wx.BLACK_PEN )
                dc.SetBrush( wx.TRANSPARENT_BRUSH )

                w = (((pos*256)/CUSTOM_COMBOBOX_ANIMATION_DURATION)*width)/256
                ratio = float(w) / float(width)
                h = int(height * ratio)
                
                dc.DrawBitmap( self.aniBackBitmap, rect.x, rect.y )
                dc.DrawRectangle( center_x - w/2, center_y - h/2, w, h )
            else:
                stopTimer = True

        if stopTimer:
            dc.DrawBitmap( self.aniBackBitmap, rect.x, rect.y )
            popup.Move( (0, 0) )
            self.aniTimer.Stop()
            self.DoShowPopup( rect, self.aniFlags )

