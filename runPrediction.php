<?php
    $State_Name = $_GET['state'];
    $District_Name = $_GET['district'];
    $Crop_Year = $_GET['year'];
    $Season = $_GET['season'];
    $Crop = $_GET['crop'];
    $Area = $_GET['area'];

    $res = shell_exec("python3 prediction.py $State_Name $District_Name $Crop_Year $Season $Crop $Area");

    echo $res;
?>