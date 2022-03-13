using NUnit.Framework;
using UnityEngine.UI;
using UnityEngine;

[Category("Slider")]
public class SliderRectRefernces : TestBehaviourBase<UnityEngine.UI.Slider>
{
    private Slider slider;
    private GameObject emptyGO;

    [SetUp]
    public override void TestSetup()
    {
        base.TestSetup();

        var rootChildGO = new GameObject("root child");
        rootChildGO.AddComponent<Canvas>();

        var sliderGameObject = new GameObject("Slider");
        slider = sliderGameObject.AddComponent<Slider>();

        emptyGO = new GameObject("base", typeof(RectTransform));

        sliderGameObject.transform.SetParent(rootChildGO.transform);
        emptyGO.transform.SetParent(sliderGameObject.transform);
    }

    [Test]
    public void AssigningSelfResultsInNullReferenceField()
    {
        slider.fillRect = (RectTransform)slider.transform;
        Assert.IsNull(slider.fillRect);

        slider.handleRect = (RectTransform)slider.transform;
        Assert.IsNull(slider.handleRect);
    }

    [Test]
    public void AssigningOtherObjectResultsInCorrectReferenceField()
    {
        slider.fillRect = (RectTransform)emptyGO.transform;
        Assert.IsNotNull(slider.fillRect);
        Assert.AreEqual(slider.fillRect, (RectTransform)emptyGO.transform);

        slider.handleRect = (RectTransform)emptyGO.transform;
        Assert.IsNotNull(slider.handleRect);
        Assert.AreEqual(slider.handleRect, (RectTransform)emptyGO.transform);
    }
}
