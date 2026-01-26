<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.44.6-Solothurn" hasScaleBasedVisibilityFlag="0" autoRefreshTime="0" minScale="1e+08" maxScale="0" autoRefreshMode="Disabled" styleCategories="LayerConfiguration|Symbology|Rendering">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
    </provider>
    <rasterrenderer alphaBand="-1" band="1" nodataColor="" classificationMax="0.8258712" type="singlebandpseudocolor" classificationMin="0.2403944" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="1" maximumValue="0.82587120000000003" minimumValue="0.24039440000000001" colorRampType="INTERPOLATED" clip="0" labelPrecision="4">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option value="215,25,28,255,rgb:0.8431373,0.0980392,0.1098039,1" name="color1" type="QString"/>
              <Option value="43,131,186,255,rgb:0.1686275,0.5137255,0.7294118,1" name="color2" type="QString"/>
              <Option value="ccw" name="direction" type="QString"/>
              <Option value="0" name="discrete" type="QString"/>
              <Option value="gradient" name="rampType" type="QString"/>
              <Option value="rgb" name="spec" type="QString"/>
              <Option value="0.25;253,174,97,255,rgb:0.9921569,0.6823529,0.3803922,1;rgb;ccw:0.5;255,255,191,255,rgb:1,1,0.7490196,1;rgb;ccw:0.75;171,221,164,255,rgb:0.6705882,0.8666667,0.6431373,1;rgb;ccw" name="stops" type="QString"/>
            </Option>
          </colorramp>
          <item alpha="255" value="0.240394398570061" color="#d7191c" label="0,2404"/>
          <item alpha="255" value="0.386763591319323" color="#fdae61" label="0,3868"/>
          <item alpha="255" value="0.533132784068584" color="#ffffbf" label="0,5331"/>
          <item alpha="255" value="0.679501976817846" color="#abdda4" label="0,6795"/>
          <item alpha="255" value="0.825871169567108" color="#2b83ba" label="0,8259"/>
          <rampLegendSettings direction="0" useContinuousLegend="1" orientation="2" maximumLabel="" suffix="" minimumLabel="" prefix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option name="decimal_separator" type="invalid"/>
                <Option value="6" name="decimals" type="int"/>
                <Option value="0" name="rounding_type" type="int"/>
                <Option value="false" name="show_plus" type="bool"/>
                <Option value="true" name="show_thousand_separator" type="bool"/>
                <Option value="false" name="show_trailing_zeros" type="bool"/>
                <Option name="thousand_separator" type="invalid"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" gamma="1" brightness="0"/>
    <huesaturation grayscaleMode="0" colorizeOn="0" colorizeRed="255" invertColors="0" saturation="0" colorizeBlue="128" colorizeStrength="100" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
