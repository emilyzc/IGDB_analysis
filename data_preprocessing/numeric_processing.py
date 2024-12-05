from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

def delete_before_filling(df):
    cols_to_drop = ['collection', 'keywords', 'similar_games', 'involved_companies_developer', 
                'involved_companies_porting', 'involved_companies_publisher', 'involved_companies_supporting', 
                'bundles']

    # Drop the columns
    newdf = df.drop(columns=cols_to_drop)
    return newdf



def process_column(df, column_name):
    # Fill NaN values in the column with the mean
    df = fill_with_median(df, column_name)
    
    # Analyze the processed column
    analyze_feature(df, column_name)
    
    # Min-max normalize the column
    df = min_max_normalize(df, column_name)
    
    return df



def fill_with_median(df, column_name):
    # Calculate the median of the column
    median_value = df[column_name].median()
    
    # Fill NaN values in the column with the median value
    df[column_name].fillna(value=median_value, inplace=True)
    
    return df



def min_max_normalize(df, feature):
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()

    # If the column contains NaN values, temporarily fill them with a placeholder
    # (for the purpose of computing min and max)
    placeholder = df[feature].mean()
    df_temp = df[feature].fillna(placeholder)

    # Compute minimum and maximum on the temporary data
    scaler.fit(df_temp.values.reshape(-1, 1))

    # Transform the original feature
    df[feature] = scaler.transform(df[[feature]])

    # Print the min and max values used for the normalization
    print(f"Min value for {feature} normalization: {scaler.data_min_[0]}")
    print(f"Max value for {feature} normalization: {scaler.data_max_[0]}")

    return df



def analyze_feature(data, feature_name):

    if feature_name in data.columns:
        min_val = data[feature_name].min()
        max_val = data[feature_name].max()

        bar_color = 'rgb(130,176,210)'


        fig = go.Figure(data=[go.Histogram(
            x=data[feature_name], 
            nbinsx=50,
            marker=dict(color=bar_color)
        )])

        # Adding annotations for min and max values
        fig.add_annotation(
            x=min_val,
            y=0,
            text=f"Min: {min_val}",
            showarrow=True,
            arrowhead=4,
            ax=0,
            ay=-40,
            bgcolor='lightgrey'
        )
        fig.add_annotation(
            x=max_val,
            y=0,
            text=f"Max: {max_val}",
            showarrow=True,
            arrowhead=4,
            ax=0,
            ay=-40,
            bgcolor='lightgrey'
        )

        fig.update_layout(
            title_text=f'Distribution of {feature_name}',
            title_font_size=20,
            font=dict(family="Helvetica", size=12),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            xaxis=dict(
                title=feature_name,
                linecolor='black',
                linewidth=2,
                # gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Count',
                linecolor='black',
                linewidth=2,
                gridcolor='lightgray'
            ),
            bargap=0.05
        )

        # Checking the skewness to decide on y-axis scale
        skewness = data[feature_name].skew()
        print(f'The skewness of {feature_name} is {skewness}')

        # If skewness is high, use a logarithmic scale for the y-axis
        if abs(skewness) > 2:
            fig.update_layout(yaxis_type="log", yaxis_title="Log(Count)")

        fig.show()
    else:
        print(f"'{feature_name}' is not a feature in your data")



def min_max_normalize_p(df, feature):

    scaler = MinMaxScaler()

    min_val = df[feature].min()
    max_val = df[feature].max()

    bar_color = 'rgb(130,176,210)'

    # Create a bar chart to show distribution before filling null values with custom styling
    fig = go.Figure(data=[go.Histogram(
        x=df[feature], 
        nbinsx=50,
        marker=dict(color=bar_color)
    )])
    
    # Adding annotations for min and max values
    fig.add_annotation(
        x=min_val,
        y=0,
        text=f"Min: {min_val}",
        showarrow=True,
        arrowhead=4,
        ax=0,
        ay=-40,
        bgcolor='lightgrey'
    )

    fig.add_annotation(
        x=max_val,
        y=0,
        text=f"Max: {max_val}",
        showarrow=True,
        arrowhead=4,
        ax=0,
        ay=-40,
        bgcolor='lightgrey'
    )

    fig.update_layout(
        title_text=f'Distribution of {feature} before filling NaN values',
        title_font_size=20,
        font=dict(family="Helvetica", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title=feature,
            linecolor='black',
            linewidth=2,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Count',
            linecolor='black',
            linewidth=2,
            gridcolor='lightgray'
        ),
        bargap=0.05
    )
    fig.show()

    # If the column contains NaN values, temporarily fill them with a placeholder
    # (for the purpose of computing min and max)
    placeholder = df[feature].mean()
    df_temp = df[feature].fillna(placeholder)

    # Compute minimum and maximum on the temporary data
    scaler.fit(df_temp.values.reshape(-1, 1))

    # Transform the original feature
    df[feature] = scaler.transform(df[[feature]])

    # Print the min and max values used for the normalization
    print(f"Min value for {feature} normalization: {scaler.data_min_[0]}")
    print(f"Max value for {feature} normalization: {scaler.data_max_[0]}")

    return df



def normalize_and_fill_median_p(df, column_name):
    # Normalize the column using Min-Max scaling
    df = min_max_normalize_p(df, column_name)
    
    # Calculate the median of the normalized column
    median_value = df[column_name].median()
    
    # Fill NaN values in the column with the median value
    df[column_name].fillna(value=median_value, inplace=True)
    
    return df