using UnityEngine;
using UnityEngine.EventSystems;

public class DragCallbackCheck : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
{
    private bool loggedOnDrag = false;
    public bool onBeginDragCalled = false;
    public bool onDragCalled = false;
    public bool onEndDragCalled = false;

    public void OnBeginDrag(PointerEventData eventData)
    {
        onBeginDragCalled = true;
    }

    public void OnDrag(PointerEventData eventData)
    {
        if (loggedOnDrag)
            return;

        loggedOnDrag = true;
        onDragCalled = true;
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        onEndDragCalled = true;
    }
}
