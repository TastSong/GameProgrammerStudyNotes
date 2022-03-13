using System.IO;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.TestTools;


namespace LayoutTests
{
    public class HorizontalLayoutGroupTests : IPrebuildSetup
    {
        GameObject m_PrefabRoot;
        const string kPrefabPath = "Assets/Resources/HorizontalLayoutGroupPrefab.prefab";

        public void Setup()
        {
#if UNITY_EDITOR
            var rootGO = new GameObject("rootGo");
            var canvasGO = new GameObject("Canvas", typeof(Canvas));
            canvasGO.transform.SetParent(rootGO.transform);

            var groupGO = new GameObject("Group", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            groupGO.transform.SetParent(canvasGO.transform);
            var horizontalLayoutGroup = groupGO.GetComponent<HorizontalLayoutGroup>();
            horizontalLayoutGroup.padding = new RectOffset(2, 4, 3, 5);
            horizontalLayoutGroup.spacing = 1;
            horizontalLayoutGroup.childForceExpandWidth = false;
            horizontalLayoutGroup.childForceExpandHeight = false;
            horizontalLayoutGroup.childControlWidth = true;
            horizontalLayoutGroup.childControlHeight = true;

            var element1GO = new GameObject("Element1", typeof(RectTransform), typeof(LayoutElement));
            element1GO.transform.SetParent(groupGO.transform);
            var layoutElement1 = element1GO.GetComponent<LayoutElement>();
            layoutElement1.minWidth = 5;
            layoutElement1.minHeight = 10;
            layoutElement1.preferredWidth = 100;
            layoutElement1.preferredHeight = 50;
            layoutElement1.flexibleWidth = 0;
            layoutElement1.flexibleHeight = 0;

            var element2GO = new GameObject("Element2", typeof(RectTransform), typeof(LayoutElement));
            element2GO.transform.SetParent(groupGO.transform);
            var layoutElement2 = element2GO.GetComponent<LayoutElement>();
            layoutElement2.minWidth = 10;
            layoutElement2.minHeight = 5;
            layoutElement2.preferredWidth = -1;
            layoutElement2.preferredHeight = -1;
            layoutElement2.flexibleWidth = 0;
            layoutElement2.flexibleHeight = 0;

            var element3GO = new GameObject("Element3", typeof(RectTransform), typeof(LayoutElement));
            element3GO.transform.SetParent(groupGO.transform);
            var layoutElement3 = element3GO.GetComponent<LayoutElement>();
            layoutElement3.minWidth = 25;
            layoutElement3.minHeight = 15;
            layoutElement3.preferredWidth = 200;
            layoutElement3.preferredHeight = 80;
            layoutElement3.flexibleWidth = 1;
            layoutElement3.flexibleHeight = 1;

            if (!Directory.Exists("Assets/Resources/"))
                Directory.CreateDirectory("Assets/Resources/");

            PrefabUtility.SaveAsPrefabAsset(rootGO, kPrefabPath);
            GameObject.DestroyImmediate(rootGO);
#endif
        }

        [SetUp]
        public void TestSetup()
        {
            m_PrefabRoot = Object.Instantiate(Resources.Load("HorizontalLayoutGroupPrefab")) as GameObject;
        }

        [TearDown]
        public void TearDown()
        {
            GameObject.DestroyImmediate(m_PrefabRoot);
        }

        [OneTimeTearDown]
        public void OneTimeTearDown()
        {
#if UNITY_EDITOR
            AssetDatabase.DeleteAsset(kPrefabPath);
#endif
        }

        [Test]
        public void TestCalculateLayoutInputHorizontal()
        {
            HorizontalLayoutGroup layoutGroup = m_PrefabRoot.GetComponentInChildren<HorizontalLayoutGroup>();
            layoutGroup.CalculateLayoutInputHorizontal();
            layoutGroup.SetLayoutHorizontal();
            layoutGroup.CalculateLayoutInputVertical();
            layoutGroup.SetLayoutVertical();

            Assert.AreEqual(48, layoutGroup.minWidth);
            Assert.AreEqual(318, layoutGroup.preferredWidth);
            Assert.AreEqual(1, layoutGroup.flexibleWidth);
        }

        [Test]
        public void TestCalculateLayoutInputVertical()
        {
            HorizontalLayoutGroup layoutGroup = m_PrefabRoot.GetComponentInChildren<HorizontalLayoutGroup>();
            layoutGroup.CalculateLayoutInputHorizontal();
            layoutGroup.SetLayoutHorizontal();
            layoutGroup.CalculateLayoutInputVertical();
            layoutGroup.SetLayoutVertical();

            Assert.AreEqual(23, layoutGroup.minHeight);
            Assert.AreEqual(88, layoutGroup.preferredHeight);
            Assert.AreEqual(1, layoutGroup.flexibleHeight);
            Assert.AreEqual(1, layoutGroup.flexibleHeight);
        }
    }
}
