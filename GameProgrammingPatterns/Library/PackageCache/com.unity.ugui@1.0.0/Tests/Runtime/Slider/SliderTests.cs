using NUnit.Framework;
using UnityEngine.UI;
using UnityEngine;

[Category("Slider")]
public class SliderTests
{
    private Slider slider;
    private GameObject emptyGO;

    [SetUp]
    public void Setup()
    {
        var rootChildGO = new GameObject("root child");
        rootChildGO.AddComponent<Canvas>();

        var sliderGameObject = new GameObject("Slider");
        slider = sliderGameObject.AddComponent<Slider>();

        emptyGO = new GameObject("base", typeof(RectTransform));

        sliderGameObject.transform.SetParent(rootChildGO.transform);
        emptyGO.transform.SetParent(sliderGameObject.transform);
    }

    [Test]
    public void SetSliderValueWithoutNotifyWillNotNotify()
    {
        slider.value = 0;

        bool calledOnValueChanged = false;

        slider.onValueChanged.AddListener(f => { calledOnValueChanged = true; });

        slider.SetValueWithoutNotify(1);

        Assert.IsTrue(slider.value == 1);
        Assert.IsFalse(calledOnValueChanged);
    }
}
